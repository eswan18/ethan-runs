module Common
  def self.cleanup_column_name(s)
    s = s.gsub('/', ' per ').gsub('(', 'in ').gsub(')', '')
    s.gsub(' ', '_').downcase
  end
  def self.cleanup_column_names(a)
    a.map{ |s| self.cleanup_column_name(s) }
  end
end
