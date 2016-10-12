TradingAppTestv2BE - Bookforex app
==================================

Description
-----------
Bookforex is a trading currency application that uses the [Fixer](http://fixer.io).


Dependencies
------------

 - Python 2.7
 - virtualenv
 - pip 
 - click
 - Flask
 - Flask-SQLAlchemy
 - itsdangerous
 - Jinja2
 - MarkupSafe
 - requests
 - SQLAlchemy
 - Werkzeug


Quickstart
----------

This application has been tested on Linux. 
The application needs access to Fixer.io for correct operation, 
but does not use internet for installation. All units are at folder packages.


To use the application you must follow these steps:

*Note: for list the options available make the script:*

       # make list


**Steps to deploy the application:**

1.  If you use virtualenv or virtualenvwrapper, first create and activate an environment, before running the setup. For example:

        # p virtualenv2 python2 env_name

        # . env_name / bin / activate

2. This will install all requirements contained at ./packages:  

        # make DESTDIR=Full_directory_to_packages' setup

3.  To create and initialize SQLite database:

        # make init-db
        

Execute app
-----------

Finally execute:

    # make run
        
To run the application on the local server, being accessible at:
    
    # http://0.0.0.0:5000

License
-------
GPL. Author: jesusropi@gmail.com

