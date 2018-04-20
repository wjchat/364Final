**Brief Description**
This app uses an api from flickr and allows users to look up cameras, save and rate them (the ratings are globally averaged), look up pictures, save the pictures, and send them to other users. 

**NOTE**
instead of base.html i use a file called base.html but it behaves as base.html

**More in-depth description**
After creating an account and logging in, the user can search pictures by key-word. Next, they can save any of these photos and view all saved photos in 'saved', in the nav bar. From here, they can unsave(delete) pictures or send them to another user. If the user selects 'messages' in the nav bar, they will see a list of sent and recieved pictures/messages. Returning to the home page by clicking 'home' in the nav bar, we can browse cameras. Select cameras and then select a brand. From here, we can see a list of all models from this brand. Enter a rating and select 'rate'. From here, the app will take you to a page that shows all of the cameras you have rated. Selecting 'all cameras' in the nav bar will take the user to a page which lists all cameras that have been saved by any user, the amount of 'votes' (how many times a camera has been rated), and a rating which has been calculated by averaging ratings from all users. This rating is updated every time the camera is rated by an individual user, as is votes.

**additional modules to be installed**
pprint
flickerapi
I think we've used everything else in class

**routes in the app**
errorhandler(404) -> 404.html
errorhandler(500) -> 500.html
/ -> login.html
/logout -> url_for login
/home -> home.html
/saved_photos -> saved_photos.html
/register -> registration.html and redirect to login page
/search_results -> search_photos.html
/messages -> messages.html
/send_photo -> send_photo.html
/cameras -> cameras.html
/models -> models.html
/all_models -> all_cameras.html
/your_models -> your_models.html

Requirements to complete for 2880 points (90%) -- an awesome, solid app
(I recommend treating this as a checklist and checking things off as you get them done!)

Documentation README Requirements
 **Create a README.md file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: **This text would be bold** and this text would not be)**

 **The README.md file should use markdown formatting and be clear / easy to read.**

 **The README.md file should include a 1-paragraph (brief OK) description of what your application does**

 **The README.md file should include a detailed explanation of how a user can user the running application (e.g. log in and see what, be able to save what, enter what, search for what... Give us examples of data to enter if it's not obviously stated in the app UI!)**

 **The README.md file should include a list of every module that must be installed with pip if it's something you installed that we didn't use in a class session. If there are none, you should note that there are no additional modules to install.**

 *The README.md file should include a list of all of the routes that exist in the app and the names of the templates each one should render OR, if a route does not render a template, what it returns (e.g. /form -> form.html, like the list we provided in the instructions for HW2 and like you had to on the midterm, or /delete -> deletes a song and redirects to index page, etc).*

Code Requirements
Note that many of these requirements of things your application must DO or must INCLUDE go together! Note also that you should read all of the requirements before making your application plan***.***

 **Ensure that your SI364final.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up). Your main file must be called SI364final.py, but of course you may include other files if you need.**

 **A user should be able to load http://localhost:5000 and see the first page they ought to see on the application.**

 **Include navigation in base.html with links (using a href tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, like this )**

 **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**

 **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).**

 **Must have data associated with a user and at least 2 routes besides logout that can only be seen by logged-in users.**

 **At least 3 model classes besides the User class.**

 **At least one one:many relationship that works properly built between 2 models.**

 **At least one many:many relationship that works properly built between 2 models.**

** Successfully save data to each table.**

 **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

 **At least one query of data using an .all() method and send the results of that query to a template.**

** At least one query of data using a .filter_by(... and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

 **At least one helper function that is not a get_or_create function should be defined and invoked in the application.**

 **At least two get_or_create functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

 **At least one error handler for a 404 error and a corresponding template.**

 **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

 **Include at least 4 template .html files in addition to the error handling template files.**

 **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.
 At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that does accord with other involved sites' Terms of Service, etc).**

 **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source to the database (in some way)**
** At least one WTForm that sends data with a GET request to a new page.**

** At least one WTForm that sends data with a POST request to the same page. (NOT counting the login or registration forms provided for you in class.)**

** At least one WTForm that sends data with a POST request to a new page. (NOT counting the login or registration forms provided for you in class.)**

 **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

** Include at least one way to update items saved in the database in the application (like in HW5).**

 **Include at least one way to delete items saved in the database in the application (also like in HW5).**

** Include at least one use of redirect.**

** Include at least two uses of url_for. (HINT: Likely you'll need to use this several times, really.)**

** Have at least 5 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.)**

Additional Requirements for additional points -- an app with extra functionality!
Note: Maximum possible % is 102%.

 (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
 (100 points) Create, run, and commit at least one migration.
 (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
 (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
 (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a specific-service account in the README, in the same section as the list of modules that must be installed.
To submit
Commit all changes to your git repository. Should include at least the files:
README.md
SI364final.py
A templates/ directory with all templates you have created inside it
May include others (e.g. may include a static folder if you are including or uploading static files, but this is not necessary!)
Your GitHub repository should be private! (Check out how to get a Student Developer Pack to do so.)
Create a GitHub account called 364final on your GitHub account. (You are NOT forking and cloning anything this time, you are creating your own repo from start to finish.)
Invite users aerenchyma (Jackie), pandeymauli (Mauli) and Watel (Sonakshi, or sonakshi@umich.edu) as collaborators on the repository. Here's the reminder of how to add a collaborator to a repository.
Submit the link to your GitHub repository to the SI 364 Final Project assignment on our Canvas site. The link should be of the form: https://github.com/YOURGITHUBUSERNAME/364final (if it doesn't look like that, you are probably linking to something specific inside the repo, so make sure it does look like that).
All set!