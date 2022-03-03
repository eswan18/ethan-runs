module EthanRuns
  module Models
    class User < ActiveRecord::Base
      self.primary_key = 'id'
    end
  end
end
