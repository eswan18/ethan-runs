# Ethan Runs

Install it:
1. Make a virtual env
2. `brew install postgresql` (if on Mac; use an appropriate package manager for your platform)
2. `make install`

Run it:
```bash
make serve
```

## Adding Activities

The easiest format to get activities in is a CSV from Under Armour's MapMyFitness site.
This CSV can be fed to the script `upload_activities.py` along with a root URL for an instance of this app.
```bash
python scripts/upload_activities.py ~/Downloads/my_workouts.csv https://ethan-runs.herokuapp.com
```
The script will interactively prompt for your username and password.
