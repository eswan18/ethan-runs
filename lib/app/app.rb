# frozen_string_literal: true

require 'active_record'
require "sinatra/base"
require "sinatra/activerecord"
require "sinatra/cors"
require_relative "./auth.rb"


module EthanRuns
  class App < Sinatra::Base
    register Sinatra::ActiveRecordExtension
    register Sinatra::Cors

    set :allow_origin, "http://localhost:1337"
    set :allow_methods, "GET,HEAD,POST"
    set :allow_headers, "content-type,if-modified-since"
    set :expose_headers, "location,link"

    before do
      begin
        if request.body.read(1)
          request.body.rewind
          @request_payload = JSON.parse request.body.read, { symbolize_names: true }
        end
      rescue JSON::ParserError => e
        request.body.rewind
        puts "The body #{request.body.read} was not JSON"
      end
    end


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
      # Get activities, optionally filtering by type.
      token = request.env['HTTP_AUTHORIZATION']
      if token != $AuthToken
        return 401
      end
      acts = Models::Activity.all
      if activity_type = params['activity_type']
        acts = acts.where(activity_type: params['activity_type'])
      end
      if start_date = params['start_date']
        acts = acts.where('workout_date >= ?', start_date)
      end
      if end_date = params['end_date']
        acts = acts.where('workout_date <= ?', end_date)
      end
      [200, acts.to_json]
    end
    post '/api/activities' do
      token = request.env['HTTP_AUTHORIZATION']
      if token != $AuthToken
        401
      end
      data = JSON.parse request.body.read
      # Fix column names to match table
      data.transform_keys! { |key| Common::normalize_column_name(key) }
      activity = Models::Activity.create(data)
      201
    end
  end
end
