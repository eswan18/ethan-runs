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
    get '/activities' do
      "#{Models::Activity.count}"
    end
  end
end
