require 'digest'

module EthanRuns
  class App < Sinatra::Base
    def secret_key
      ENV.fetch('APP_SECRET')
    end

    def auth_hash(username:, password:)
      string_to_be_hashed = "#{secret_key}:#{username}:#{password}"
      Digest::SHA256.hexdigest string_to_be_hashed
    end

    post '/api/auth' do
      params = @request_payload[:credentials]
      username = params[:username]
      password = params[:password]
      pw_hash = auth_hash(username: username, password: password)
      user = Models::User.where(username: username).first
      if pw_hash == user[:pw_hash]
        a = Models::AuthToken.new
      else
        return 401, "Incorrect username/password"
      end
    end
  end
end
