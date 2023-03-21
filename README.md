# Finlog
This is a financial tracker web-app developed as final project for CS50 course.
#### Video demo: https://www.youtube.com/watch?v=jHu4dAoeUZ4

It is developed with: 
- Python & Django
- JavaScript & JQuery
- HTML 
- CSS

For style and visuals:
- Bootstrap (https://getbootstrap.com/)
- Popper (https://popper.js.org/)
- Font awesome icons (https://fontawesome.com/start)

# Features
- REGISTER & LOG IN with created username/password.

- LOG allows user to create notes about his expenses with CATEGORY and optional comment. Log entries can be sorted to display all of them, or just expenses made this month or today. 

![image](https://user-images.githubusercontent.com/119735427/226408180-6b502f2e-ebd4-4f13-9167-43e5a81e8d54.png)

- CATEGORIES: app features few default categories and allows user to change them, recolor and also create new categories .

![image](https://user-images.githubusercontent.com/119735427/226410744-d64cc406-ae41-4ac3-a0e8-108434204fbe.png)

- CURRENCY & BUDGET: settings window allows user to set up a budget for a month and choose currency in which prices will be displayed and new entries created. 

 ![image](https://user-images.githubusercontent.com/119735427/226409316-9f9cef56-5066-41a2-bc60-7445f67480cc.png)

When user exceeds monthly budget, they will be notified with a red budget icon. At any moment user can check, how much they spent this month. 

![image](https://user-images.githubusercontent.com/119735427/226409730-942f7c01-b988-4d97-a730-257dfe85b813.png)

# Choises

Since CS50 requires some explanation on choises I made during the developement, here it is :)

#### Platform
I enjoyed developing stock trading app for CS50 homework (and put in it quite a lot of effort as well) and decided that web-app is just what I need. Idea of an app was suggested by chat-GPT (also it helped a lot with debugging during the developement) and I chose Django to make sure I learn something new during this project ;)
Studying it purely from Django documentation was not easy should I say, especially because english is not my native language, and there is no documentation on russian.

#### Apps
I decided to split my application to two separate apps (as Django documentation advise to do) at least because I needed to study how it works.
This was quite a controversial decision, because separate apps complicated things like loading static files and using template system a lot. I did learn quite a bit from it though.
My two apps are accounts and log. Accounts are responsible for registering, logging user in and out. Also accounts holds custom user models and user categories, that are generated from default ones at user creation. Log is responsible for showing actual Finlog main page and allows to create, delete entries, edit settings and customize categories.

#### Dependencies & sources
As CS50 advised I used Bootstrap (and Poppers.js) to make front-end look nice without effort, however it required a lot of effort anyway since I did not know a lot about CSS and HTML at the beginning of developement. However at the end of it, it became much easier, I even made app adaptive for different screens and even phones. 
For icons I used Fontawesome, and will sure use them in future, they look simple and great.
For some interactions with page I used JQuery, in order to learn it as well. 
Database is using SQLite3, which is default for Django. I didn't need to use actual SQL though, Django did everything, I only had to create right python classes for my models.
I hosted my app on pythonanywhere.com (where it is avaliable at the moment), it took quite some time to set up and deploy, but at the end it works great. And it is free!

#### Structure
Naturally my web-app has a back-end and front-end. Backend code is mostly written in views.py with use of functions to load/sort/create objects in helpers.py. Quite some time I spent deciding which models to create, how to connect them and in which app to place them. After a lot of attempts and tries I decided to create Category model in Log app, which would represent default app's categories, and in the Accounts app I made custom User model that is derivative of default Django's User. Each User object has UserCategory objects, that are customised Category objects or new ones and Entry objects which have foreign keys on UserCategory & User and represent a spending User does.
About half of all the code in project is in JavaScript, there are functions to load the log, show adding and deleting entries on the page, updating categories, budged etc. I was surprised how much JavaScript requires even a Python app. 
For sending requests to the server from the page I used all the avaliable options: AJAX requests, XML requests and Fetch() functions to learn how to use each of them. From what I've seen I can make a conclusion that fetch() is most simple and useful of them, at least for my purposes: send JSON to the server, get response, parse it and catch errors.
