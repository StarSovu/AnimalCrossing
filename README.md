# AnimalCrossing
tsoha 2020

Tehtävä ennen sunnuntain palautusta:
Admin-sivu jolla:
Annetaan hahmolle nimi, valitaan hahmolle laji, persoonallisuus ja asu (valinnat radio-button) sekä annetaan syntymäpäivä. Tarkastetaan että kaikki tiedot on annettu, ei saa jäädä mikään kenttä tyhjäksi. Laitetaan myös visible = 1.
Admin-sivu jolla (voi olla sama kuin edellinen sivu?):
Muokataan olemassa olevia hahmoja (nimen muutos, syntymäpäivän muutos, lajin, persoonallisuuden ja asun vaihtaminen) 
User-sivu jolla:
valitaan saarelle hahmot ja asut
Päivitetään readme.md; Animal Crossing kuvaus ja ohjelman toimintaa tarkemmin.




Animal Crossing is a social simulation video game series by Nintendo. In Animal Crossing, the player character is a human who lives in a village inhabited by various anthropomorphic animals, carrying out various activities such as fishing, bug catching, and fossil hunting. The series is notable for its open-ended gameplay and extensive use of the video game console's internal clock and calendar to simulate real passage of time. (Description based on Wikipedia article.) This application is particularly based on the newest game in the series, Animal Crossing: New Horizons, in which the player lives on an island with up to ten animal villagers.

This application is for users to create their own island and select their ideal roster of Animal Crossing characters for their island. Application can be tested at https://xxxxxx.herokuapp.com/

Each user has a username (unique) and password. Users can name islands for themselves, not necessarily unique names (several users can have an island with the same name). Each user can have multiple islands, every island from the same user must have a different name, and each island can have a maximum of 10 animals. Same animal can be selected on the same island only once.
(Not yet done! Limit the number of islands / user.)

Only a user with admin rights can create and edit characters. All users can select and change characters for their own island. If the island is full and the user tries to add another character, they will get a message saying that they need to kick someone off their island before they can add another character. Users cannot have the same character multiple times, but multiple users can have the same character on their island. Users can view other user's islands and the selected animals on them.

(Not yet done!)
Admin can hide users, islands, characters and character parameters.

Characters have: name (unique), birthday (month and day)(birthday not yet done!), species, personality and outfit. Only user with admin rights can select birthday (not yet done!), species, personality and outfit for characters. (This not yet done!) Users can change the outfit for a character on a specific island. If the same animal is on multiple islands, it can have different outfit on different islands.


(This not yet done!) Any visitor can see the list of charactes and filter it by species and/or personality. Lists can be arranged alphabetically or by birthday. There is also a search function, which allows visitors to search for characters with specific names. Visitors can see for which islands each character is selected to.

Optional, after other features of the application have been compeleted:
There are also outfits, which users can give to animals on their island. Each animal has a specific default outfit which they wear if the user does not change them. Each animal can only wear one outfit, but the same outfit can be given to multiple animals. , so users cannot change animals' outfits on other islands.


Application utlizes a database. In database there are tables:

users:
username - Password hash value(not yet done, just password as text!) - role(user/admin) - visible (0/1)

outfits:
id - outfitname - visible (0/1)

personalities:
id - personalityname - visible (0/1)

species:
id - speciesname - visible (0/1)

characters:
id - charactername - speciesid - personalityid - outfitid- birthday (MM/DD) - visible (0/1)

islands:
id - islandname - userid - visible (0/1)

characteronisland:
island id- characterid - outfitid - visible (0/1)


On the index.html site it is checked if user is logged in or not. If not, login and register possibilities are shown. Before login users need to register. For user named 'admin' role 'admin' role is given directly in SQL, not by this application. Users automatically are given 'user' role. When registering it is checked that the username does not yet exists.

After login user is directed to user's welcome page. From there user follows links to be able to view, create and edit their own islands. 

At the moment user passwords are saved as text in the database, this will need to be changed to hash value. At the moment not all input formats are checked, it is for example possible to give blank values as input. This will need to be changed.

Also looks and usability need improvements.


