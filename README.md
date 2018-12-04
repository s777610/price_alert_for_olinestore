# Price Alert for Online Store

## The URL of this Web App:
## https://priceing-alerts.herokuapp.com/

This is a web application, which is able to track the price of items from the online store.  
The application can notify users when the prices of items drop.
The application checks the prices every 10 minutes.
All data is stored in database, which is MongoDB in this case.
All passwords of users are encrypted by pbkdf2.
Utilizing regular expression to find the specific store for users
The price of item could be found by using beautifulsoup to parse html

## Installation
```
pipenv install
```
### Make sure you have MongoDB installed before running the application
1. Run MongoDB server locally
```
mongod
```
2. Create the MongoDB instance and connect to the server
```
mongo
```

Notice:  This Web application uses Mailgun API to send the email to users in order to notify them when the price drop.
The details of Mailgun account and API key should be put into src/models/alerts.constants.py.

This web application only allows administrators(src/config.py) to add, remove and edit online stores.

**How to use this Web?**
1. Users have to register on the web.
2. Users have to add the URL of the item which you want to track and the name of the items.
3. Users have to add the limit price they intend to buy.
4. When the price drops, users will be notified by email.
5. Users are able to edit, activate, deactivate and delete alerts.


## 1. This is home page, which allow users to register, longin and see the supporting stores
<img width="1018" alt="screen shot 2018-07-03 at 12 33 48 pm" src="https://user-images.githubusercontent.com/35472776/42240926-bb972a52-7ebd-11e8-9c0a-3635327f526c.png">

## 2. This is the supporting stores page, shows users that what stores are available right now.
<img width="806" alt="screen shot 2018-07-03 at 12 34 34 pm" src="https://user-images.githubusercontent.com/35472776/42240978-e34aab50-7ebd-11e8-97a7-549067cc10c2.png">

## 3. This is user-alerts page, shows alerts all alerts they have created. Then, right click alert can edit, activate, deactivate and delete the alert.
<img width="781" alt="screen shot 2018-07-03 at 12 34 52 pm" src="https://user-images.githubusercontent.com/35472776/42240999-f71d3ec2-7ebd-11e8-8a85-5d1b73f4f0a6.png">

## 4. This page allows users to create the new alert.
<img width="764" alt="screen shot 2018-07-03 at 12 35 04 pm" src="https://user-images.githubusercontent.com/35472776/42241028-0e549996-7ebe-11e8-9550-88866bd5fb45.png">

## 5. This page allows admins to create the supporting stores. The admins have to pass the tag name and query of that item.
The normal user is not able to access this page for security reasons.
<img width="767" alt="screen shot 2018-07-03 at 12 35 53 pm" src="https://user-images.githubusercontent.com/35472776/42241055-21f3a5be-7ebe-11e8-9b3f-6b22fbf2aa15.png">
