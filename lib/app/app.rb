# frozen_string_literal: true

require 'active_record'
require "sinatra/base"
require "sinatra/activerecord"

module EthanRuns
  class App < Sinatra::Base
    register Sinatra::ActiveRecordExtension
    get '/' do
      'Hello Ethan!'
    end
    get '/hello/:name' do |name|
      "Hello #{name}!"
    end
    get '/api/activities/count' do
      "#{Models::Activity.count}"
    end
    post '/api/activities' do
      activity = Models::Activity.new
      activity.from_json(request.body.read)
      activity.save
      201
    end
  end
end
