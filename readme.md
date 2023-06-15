This is the readme file for MongoDB Project of Group 3 for ISTE610- Non Relational data Management

Group Members :
    1) Arun Kanjirakkad Murali
    2) Rebekah Vikram Katari
    3) Omkar Vivek Kulkarni

Our Project is a simple web baased application that uses the Tweets of the Jan 6, 2021 Capitol riots.
We have taken the database from Kaggle and it contains around 80,000 tweets around Jan 6 along with Location,
and images around the locations.

Our project is simple regex based search application which can be used to search keywords in the text of the tweets,
Aprat from that users can also search based on Latitute and Longitude to narrow down the search results based on location.

After searching the user is presented with a list of documents and user can click on one to view its contents. User has an
Option to post comments on the tweets.

User can also view all the images associated with the location from where the tweet was posted.

Technologies used to create this application are:

Frontend:
    1) HTML5
    2) CSS3
    3) JavaScript

Backend:
    1) MongoDB
    2) Python
    3) Flask
    4) GridFS

We are using Flask framework with Python script to load data to and from our mongoDB database, GridFS is used to store our images.
For displaying the data on the web browser we have JavaScript to make the page interactive and basic HTML and CSS.

To Run our application simply run the app.py file in the directory this file will create a localhost server on port 5000.
Then navigate to http://127.0.0.1:5000/ to use the application.

By default the MongoDB connection has been set to localhost i.e. 27017 use can change this in app.py along with the default database and
collection.


Thank You
Team ROA.