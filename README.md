# AnimalCrossing
tsoha 2020


Animal Crossing is a social simulation video game series by Nintendo. In Animal Crossing, the player character is a human who lives in a village inhabited by various anthropomorphic animals, carrying out various activities such as fishing, bug catching, and fossil hunting. The series is notable for its open-ended gameplay and extensive use of the video game console's internal clock and calendar to simulate real passage of time. (Description based on Wikipedia article.) This application is particularly based on the newest game in the series, Animal Crossing: New Horizons, in which the player lives on an island with up to ten animal villagers.

This application is for users to create their own island and select their ideal roster of Animal Crossing characters for their island. Application can be tested at https://tsoha-animalcrossing.herokuapp.com/. When you login as admin (user 'admin' password 'kakku' - this password is mentioned here for testing purposes and will be changed later) you will be guided to an admin page where you can add and edit characters and all of the parameters related to characters (except birthday which is not yet implemented - currently characters have the default birthday value 101 which is not used anywhere). Admin is not yet capabable of doing anything to users. You can login as 'guest' password 'password' to check an example user page where islands have already been created. You can also register a new user and start from scratch to create islands. Without login you can see the list of characters by using the link on the index page.

Each user has a username (unique) and password. Users can name islands for themselves. Several users can have an island with the same name, but the same user can only have one island with a specific name. Each user can have multiple islands, every island from the same user must have a different name.
(Number of characters on island not yet limited.)

All users can select and change characters for their own island. Islands cannot have the same character multiple times, but multiple islands can have the same character. Users can view other user's islands and the selected animals on them. Users can change the outfit for a character on a specific island. If the same animal is on multiple islands, it can have a different outfit on different islands. Multiple characters on an island can have the same outfit. The owner of an island can also remove characters from the island. If a previously removed character is added back, they will wear the outfit which they did at the time of the removal.

If the island already has 10 characters and the user tries to add another character, they will get a message saying that they need to kick someone off their island before they can add another character (not yet done - currently islands can have an unlimited number of characters).

Only a user with admin rights can create and edit characters.

(Not yet done!)
Admin can hide users, islands, characters and character parameters.

Characters have: name (unique), birthday (month and day)(birthday not yet done!), species, personality and default outfit. Only user with admin rights can select birthday (not yet done!), species, personality and outfit for characters. The default outfit is the outfit the character wears on an island when they are first added.


(This not yet done!) Any visitor can see the list of charactes and filter it by species and/or personality. Lists can be arranged alphabetically or by birthday. There is also a search function, which allows visitors to search for characters with specific names. Visitors can see for which islands each character is selected to.


Application utlizes a database. In database there are tables:

users:
username - Password (hash value) - role(user/admin) - visible (0/1)

outfits:
id - outfitname - visible (0/1)

personalities:
id - personalityname - visible (0/1)

species:
id - speciesname - visible (0/1)

characters:
id - charactername - speciesid - personalityid - outfitid - birthmmdd - visible (0/1)

islands:
id - islandname - userid - visible (0/1)

characteronisland:
island id - characterid - outfitid - visible (0/1)


On the index.html site it is checked if user is logged in or not. If not, login and register possibilities are shown. Before login users need to register. For user named 'admin' role 'admin' role is given directly in SQL, not by this application. Users are automatically given 'user' role. When registering it is checked that the username does not yet exists. Password is checked by using hash check, so passwords are not stored in the databes.

After login user is directed to user's welcome page. From there user follows links to be able to view, create and edit their own islands.

At the moment not all input formats are checked, it is for example possible to give blank values as input. This will need to be changed.

Also looks and usability need improvements.


