# frozen_string_literal: true

require 'active_record'
require "sinatra/base"
require "sinatra/activerecord"
require_relative "../models/activity"

# ActiveRecord::Base.establish_connection(db_configuration["development"])

module EthanRuns
  class App < Sinatra::Base
    register Sinatra::ActiveRecordExtension
    get '/' do
      'Hello Ethan!'
    end
    get '/hello/:name' do |name|
      "Hello #{name}!"
    end
    get '/activities' do
      Activity.all
    end
  end
end
