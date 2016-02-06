#!/usr/bin/env ruby

require 'tqdm'
require 'octokit'

def token
  File.open 'gh-access-token' do |file|
    file.read.chomp
  end
end

Client = Octokit::Client.new(access_token: token)

class Status
  def initialize(info)
    @info = info
  end

  def travis_ci_statuses
    @info
      .select { |s| s[:target_url] =~ /travis-ci\.org/ }
  end

  def most_recent
    travis_ci_statuses.first
  end

  def state
    most_recent && most_recent[:state].to_sym
  end
end

def fetch_status(name, commit)
  limit = Client.rate_limit
  if limit.remaining <= 10
    delay = limit.resets_in
    puts "Rate limit low. Blocking for #{delay} seconds..."
    sleep delay
  end

  fetch_status!(name, commit)
end

def fetch_status!(name, commit)
  Status.new(Client.statuses(name, commit))
end

def print_status(status)
  case status.state
  when :success
    puts "It succeeded!"
  when :failure
    puts "It failed."
  else
    puts "It's unaccounted for."
  end
end

status = fetch_status 'eddieantonio/isri-ocr-evaluation-tools', 'afffedade370a69234394e918f7b3edaa9353d58'
print_status status

status = fetch_status 'eddieantonio/isri-ocr-evaluation-tools', '474a9b9004f0d34ddfd31978adc3bc03a9e9e9bb'
print_status status
