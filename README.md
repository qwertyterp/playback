# playback
playing with spotify api and flask

vercel link: https://playback-smoky.vercel.app/

Description of your final project:
The final project uses Spotify API to index every artist, album and track within the spotify database and allows users to leave reviews 
under any found album. The user can search for artists on the main page, then navigate to that artists list of albums, and then see all tracks 
of that album within the album page. A user can login to leave a review, or simply just read user reviews of albums. Originally, I wanted to 
use some the Spotify Web Playback SDK, however, I found some difficulty implementing that. If I make a pretty-fied version of the application,
then I will try to add that spotify playback option. Also, I found that I didn't need to use discogs API since Spotify API was pretty extensive.
In fact, Spotify probably has just about an extensive of a catalog.

Describe what functionality is only be available to logged-in users:
Only users can leave reviews for albums. Un-logged users can only view reviews. Logged-in users can also change their username and upload a 
profile picture. 

List and describe at least 4 forms:
- SearchForm allows the user to search artists using Spotify API
- AlbumReviewForm allows logged in users to leave comment reviews under each alumn
- RegistrationForm allows the end user to register for the site
- LoginForm allows the user to login to the website
- UpdateUsernameForm allows the user to update their username
- UpdateProfilePicForm allows the user to update their profile picture

List and describe your routes/blueprints:
- main blueprint is where most of the functionality of the site comes in. How one can search for artists, navigate their albums, see their tracks.
It routes to the pages where non-logged in users can view
- user blueprint contains everything regarding user management such as login, registration, and account profile page

Describe what is stored/retrieved from MongoDB:
- album reviews
- user profile including profile picture and username + password

 Describe what Python package or API you used and how it affects the user experience:
 - I used the Spotify API search for artists, find all of their albums, and all of their tracks.
 - The API also includes many useful information such as release date, album art, track length,
   popularity, genre, etc.
