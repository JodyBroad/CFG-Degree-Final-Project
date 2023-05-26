# CFG-Degree-Final-Project
CFG Degree Final Project
Team members:
- Jody Broad
- Rada Kanchananupradit
- Melissa Long
- Georgina Annett
- Khadija Warsama

# To run our project:

1. Clone this repo onto your machine
2. The first time you run it **only** you will need to create a database called "CFGFinalProject" in MySQL Workbench - just open a new query and enter "CREATE database CFGFinalProject;" once you have run this statement and can see the database has been created you can close MySQL and will not need it further
3. In app.py you will need to update the root password in line 16, which starts: app.config['SQLALCHEMY_DATABASE_URI'] to whatever your root password is for your MySQL connection
4. Just run app.py!

## Requirements (also in requirements.txt):
- Flask==2.3.2
- flask_sqlalchemy==3.0.3
- Flask_WTF==1.1.1
- Requests==2.31.0
- WTForms==3.0.1
