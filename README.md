# Introduction

Chatbot for $%&ZLSUR&%$

### Steps to execute the code and use the app.

_The below step (first bullet point) is optional if you use the existing virtual environment (which you can activate by running command "source venv/bin/activate" from the root folder of the repo/project)_

#### Step1: Assuming python3 (preferably python 3.8.2) is installed in the machine, you need to run the following commands (may use "sudo") from the root folder of the repo/project:

- pip3 install -r requirement.txt
- python3 -m nltk.downloader stopwords  (mandatory for the first time installation)
______________________________________________

_The below two steps are optional if you continue with present database i.e. sqlite (schema & data are already there in the repo/project folder)_

#### Step2: To create the table schemas in the database (sqlite by default, can be configurable in Chatbotforwip/settings.ini by changing the connection string and installing the required python dependencies for the database), run the following command:

bash migrate.sh
______________________________________________

#### Step3: Open the sql files:
1. login.sql
2. question_answer.sql

Then, execute the scripts one by one by openning (or connecting) Chatbotforwip/static/chatbotforpro.db file in your sql workbench (or client)
______________________________________________

#### Step4: After successful addition of default and user data for log-in as stated above, execute the following command from the root folder of the repo/project:

python3 wsgi.py  (or "venv/bin/python wsgi.py" if using virtual environment)
______________________________________________

#### Step5: Finally, browse the app in Browser (preferably Google Chrome:latest) by hitting the url -> http://localhost:5000/

Login into the app using the below credentials

- Enter your email: user_test@mail.com
- Enter your password: 123456
______________________________________________

Thank you !
