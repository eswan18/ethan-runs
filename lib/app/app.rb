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
    get '/api/activities' do
      token = request.env['HTTP_AUTHORIZATION']
      if token != $AuthToken
        401
      else
        [200, Models::Activity.all.to_json]
      end
    end
    post '/api/activities' do
      token = request.env['HTTP_AUTHORIZATION']
      if token != $AuthToken
        401
      else
        activity = Models::Activity.new
        activity.from_json(request.body.read)
        activity.save
        201
      end
    end
  end
end
