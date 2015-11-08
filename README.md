# HitchBOTnet
REST API for HitchDroid tracking and logging.

HitchBOTnet requires Flask to run. http://flask.pocoo.org/

# Installation
1. Clone this repository
2. Using virtualenv is recommended
3. Install Flask `pip install Flask`
4. Change the configuration settings at the top of `hitchbotnet.py`
5. Create the database by running `from hitchbotnet import init_db` and `init_db()` in a Python shell
6. Start the server `python hitchbotnet.py`
