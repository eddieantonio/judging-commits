#!/usr/bin/env ruby

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

require 'csv'
require 'set'
require 'tqdm'
require 'travis'

# Fetch token from current working directory.
def token
  File.open 'travis-token' do |file|
    file.read.chomp
  end
rescue Errno::ENOENT => e
  $stderr.puts <<EOF
Travis-CI token not found! To obtain it, do the following:

    $ travis login
    $ travis token > travis-token
  
EOF
  raise e
end
Travis.access_token = token


Commit = Struct.new(:repo, :sha, :status)

class Repository
  attr_reader :name
  def initialize(name)
    @repo = Travis::Repository.find(name)
    @name = name
    @commits = Set.new
  end

  def each_commit_with_status
    @repo.builds.each do |build|
      sha = build.commit.sha
      next if @commits.include?(sha)
      @commits << sha

      yield Commit.new(name, sha, build.state)
    end
  end
end

def fetch_repo_names
  projects = Set.new

  options = {
    headers: false,     # No headers from the online dump
    quote_char: "\r",   # Ignore any quotes (preprocessing steps ensure that
                        # CR is not present in the string, thus setting it to
                        # quote_char will never trigger quote parsing).
    encoding: 'UTF-8'
  }
  CSV.foreach('commits.csv', options) do |row|
    name = row[0]
    projects << name
  end

  projects
end

def main
  repos = fetch_repo_names

  CSV.open('commit-status.csv', 'wb') do |output|
    repos.with_progress.each do |name|
      begin
        repo = Repository.new(name)
      rescue Travis::Client::NotFound
        $stderr.puts " [!] Could not find repository #{name}"
        next
      end

      repo.each_commit_with_status do |commit|
        output << [name, commit.sha, commit.status]
      end
    end
  end
end

main if __FILE__ == $PROGRAM_NAME
