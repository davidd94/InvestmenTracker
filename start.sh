workon InvestmenTracker
gunicorn --workers 3 --bind unix:investmentracker.sock -m 007 investmentracker.py
deactivate
