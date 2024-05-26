## Description
This project fetches unread emails from gmail and then stores in database. Based on some rules defined in email_processing_rules.json, it processes email and take some actions eg: moving the email in promotion/social.


## Prerequisites
1. Enable and add your Google Cloud Console Gmail API `credentials.json` in the repo directory. Necessary scope for the API creds: ['https://www.googleapis.com/auth/gmail.modify']
2. Setup `rules.json` at `email_processor/service/rules.json`. Sample rules JSON present for reference.
3. Install nessary requirements with this command `python3 -m pip install -r requirements.txt`


## Steps to Execute
1. Execute `python main.py`

## Steps to execute tests
1. Tests are written in tests folder
2. Exceute `python -m unittest tests/test_fetch_email.py` to run fetch_email.py tests
3. Exceute `python -m unittest tests/test_email_processor.py` to run tests for email_processor script
