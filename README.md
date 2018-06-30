The URL of this Web App: https://priceing-alerts.herokuapp.com/

This is a web application, which is able to track the price of items from the online store.  
The application can notify users when the prices of items drop. 
The application checks the prices every 10 minutes. 
All data is stored in database, which is MongoDB in this case.
All passwords of users are encrypted by pbkdf2. 

Notice:  This Web application uses Mailgun API to send the email to users in order to notify them when the price drop. 
The details of Mailgun account and API key should be put into src/models/alerts.constants.py.

This web application only allows administrators(src/config.py) to add, remove and edit online stores.

**How to use this Web?**
1. Users have to register on the web.
2. Users have to add the URL of the item which you want to track and the name of the items.
3. Users have to add the limit price they intend to buy.
4. When the price drops, users will be notified by email.
5. Users are able to edit, activate, deactivate and delete alerts.
