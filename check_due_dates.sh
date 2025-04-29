#!/bin/bash

# Change to the project directory
cd /Users/rorykretzer/project-a-28

# Activate the virtual environment
source venv/bin/activate

# Run the Django command
python manage.py check_due_dates

# Deactivate the virtual environment
deactivate 