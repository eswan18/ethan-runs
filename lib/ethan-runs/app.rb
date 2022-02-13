# frozen_string_literal: true

require "sinatra/base"
# require "sinatra/param"

module EthanRuns
  class App < Sinatra::Base
    get '/' do
      'Hello Ethan!'
    end
    get '/:name' do |name|
      "Hello #{name}!"
    end
  end
end
