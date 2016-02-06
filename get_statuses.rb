#!/usr/bin/env ruby

require 'tqdm'
require 'octokit'
require 'csv'

def token
  File.open 'gh-access-token' do |file|
    file.read.chomp
  end
end

Client = Octokit::Client.new(access_token: token)

Status = Struct.new(:statuses) do
  def travis_ci_statuses
    statuses.select { |s| s[:target_url] =~ /travis-ci\.org/ }
  end

  def most_recent
    travis_ci_statuses.first
  end

  # Returns nil if there is no status, otherwise
  # :success, :failure, :pending
  def state
    most_recent && most_recent[:state]
  end
end

Commit = Struct.new(:repo, :sha) do
  def fetch_status
    limit = Client.rate_limit
    if limit.remaining <= 10
      delay = limit.resets_in
      puts "Rate limit low. Blocking for #{delay} seconds..."
      sleep delay
    end

    fetch_status!
  end

  def fetch_status!
    Status.new(Client.statuses(repo, sha))
  rescue Octokit::NotFound
    nil
  end
end

CSV.open('commit-status.csv', 'wb') do |output|
  CSV.open('data.csv', 'rb', headers: true, encoding: 'UTF-8') do |infile|
    infile.to_enum.with_progress.each do |row|
      commit = Commit.new(row[0], row[1])
      status = commit.fetch_status
      # Either gives state or not found
      str_status = (status && status.state) || 'not_found'
      output << [commit.repo, commit.sha, str_status]
    end
  end
end
