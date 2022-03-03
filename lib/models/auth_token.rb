module EthanRuns
  module Models
    class AuthToken < ActiveRecord::Base
      self.table_name = "auth_tokens"
    end
  end
end
