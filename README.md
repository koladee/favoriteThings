# FAVORITE THINGS TRACKER


A "Favorite Things Tracker" is a system that allows the user to track or take note of things which include people, places, foods, events, etc with the use of a web app.
 


## Approach to Problem Statement
* Three different database tables were used to implement this, the User, the Category and the List tables.

* The User table is used to manage users' details such as id, username, email address, and password (password was added because any user's favorite thing has to be confidential and protected). 

* The Category table is used manage the default categories (Places, People  and Food) and also to manage the categories that will be created by other users (kindly note that any new category created by a user is visible to only that user and only this user can make use of it). The columns present in the Category table include (id, name, user_id). 

* The List table helps to manage the list of favorite things by all users, it has the following columns (id, rid, title, description, ranking, user_id, cat, created_date, modified_date and log).

##Scope

When a new favorite things is to be added by a particular user, the following conditions where satisfied:

* User must be logged in

* The description can either be empty or its length must be greater than or equal to 10 characters.

* The user can select from the following list of categories People, Place, Food and all  other categories created by this user.

* When a ranking value is submitted, the system checks through the List table for the favorite things added by this particular user with the same category submitted, if any of the favorite things checked for has the same ranking value with the newly submitted favorite thing, the ranking number of the existing favorite thing changes to the sum of the highest ranking in that category for the particular user and one. Thus, the newly submitted favorite thing maintains its own ranking value.


##Features of the solution
*  A REST API built with flask-restful with three endpoints (listed in the API endpoint section) which can handle GET, POST and PUT requests.
* User login implemented with flask-login
* SQLAlchemy ORM used for querying the database
* Password encryption using Bcrypt
* MySQL database
* Bootstrap framework used for the UI
* Jquery Javascript framework used

## How to get Started

The instructions bellow will get this project up and running on your pc (type in all commands in your command line, haven navigated to th project directory on your)

* Step 1 

Install packages

```
$ pip install -r requirements.txt
```
* Step 2

Initialize Virtual Environment
```
$ venv/bin/activate
```
* Step 3

`from the root directory from the project run the following command`

```
python favorite_things
```

favorite_things in this regards is the package name for the web app

* Step 4

You can now start interacting with the web app

`URL: ` <http://localhost:5000> 

#### API ENDPOINTS ON LOCALHOST
`User: ` <http://localhost:5000/api/user> You can `GET` , `POST` and `PUT` 

`Category: ` <http://localhost:5000/api/cat> You can `GET` , `POST` and `PUT` 

`FavoriteList: ` <http://localhost:5000/api/list> You can `GET` , `POST` and `PUT` 



## Live Version

`To setup on a live server follow this link:`
* [SEVER SETUP](https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/) - deployment with apache
* Then setup HTTP(S) load balancing to serve over port 443

`For live testing, visit`
<https://spibes.com/>

#### API ENDPOINTS ON LOCALHOST
`User: ` <https://spibes.com/api/user> You can `GET` , `POST` and `PUT` 

`Category: ` <https://spibes.com/api/cat> You can `GET` , `POST` and `PUT` 

`FavoriteList: ` <https://spibes.com/api/list> You can `GET` , `POST` and `PUT` 

## Built With

* [Flask](http://flask.pocoo.org/) - Python web framework used
* [GCP (Compute Engine)](https://console.cloud.google.com/) - Hosting Platform
* [Jquery](https://jquery.com/) - Javascript framework

