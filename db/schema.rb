# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 0) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "activity_fact", id: false, force: :cascade do |t|
    t.date "date_submitted"
    t.date "workout_date"
    t.text "activity_type"
    t.integer "calories_burned_in_kcal"
    t.float "distance_in_mi"
    t.integer "workout_time_in_seconds"
    t.float "avg_pace_in_min_per_mi"
    t.float "max_pace_in_min_per_mi"
    t.float "avg_speed_in_mi_per_h"
    t.float "max_speed_in_mi_per_h"
    t.integer "avg_heart_rate"
    t.integer "steps"
    t.binary "notes"
    t.text "source"
    t.text "link"
  end

end
