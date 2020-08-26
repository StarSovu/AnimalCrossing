# AnimalCrossing - tsoha 2020

## About
Animal Crossing is a social simulation video game series by Nintendo. In Animal Crossing, the player character is a human who lives in a village inhabited by various anthropomorphic animals, carrying out various activities such as fishing, bug catching, and fossil hunting. The series is notable for its open-ended gameplay and extensive use of the video game console's internal clock and calendar to simulate real passage of time. (Description based on Wikipedia article.)

This application is particularly based on the newest game in the series, Animal Crossing: New Horizons, in which the player lives on an island named by the player with up to ten animal villagers. The purpose of this application is to let users showcase their ideal character roster for islands.

Application is available here: https://tsoha-animalcrossing.herokuapp.com/

## Usage

### Logging in / registering
When the user first enters, they have the choice to either log in or register. When the user registers, they need to enter a username between 3 and 30 characters and a password between 4 and 256 characters. Trying to register with a username that already exists or failing to meet the requirements gives them an error message and lets them try again. Similarly, trying to log in with the incorrect password or a username that does not exists gives a message and the user gets to try again.

Logging in is required for creating islands and choosing characters for them, as each island is linked to a specific account.

### Islands
Islands can be created by any user. At the moment, there is no limit to how many islands a user can have. The user can create a new island by typing a new name for the island on the "Manage islands" page. The same user can only create one island with a specific name, but multiple users can make islands with the same name. The length of an island's name is currently not limited, but has to be at least one character. The island's creator can change the island's name afterwards.

The creator of an island can add new characters on an island, as well as remove (hide) them and change their outfits. Changing a character's outfit on a specific island does not affect their outfit elsewhere. An island can have up to ten characters added to it. Each character can only be featured once on the same island, and can only wear one outfit at a time. Multiple characters can wear the same outfit.

Other users and accounts which are not logged in are able to view islands, but they cannot edit islands which they did not create. Island pages are accessible by id numbers.

### Characters
Characters from Animal Crossing are featured in this application. Each character has their own page with their information, which includes their name, personality, species, birthday and default outfit. Characters cannot be edited by regular users.

All characters can be found in a character list. The character list can be filtered based on species, personality or month of birth, but only one of the three at a time.

### Admin
Users with admin rights can add and edit characters, as well as add new personalities, species and outfits. Admins have access to pages which are forbidden for regular users which allow doing these actions. Logging in as an admin redirects to an admin page.

Giving admin rights to other users is currently not possible in this application.

## Testing
The following accounts are available for testing:
* Username: guest, password: password (regular user)
* Username: admin, password: kakku (admin, allows testers to test adding/editing characters)

## Database
The following database tables with the following fields are used in the application:

* users: id - username - password (hash value) - role (user/admin) - visible (0/1)
* outfits: id - outfitname - visible (0/1)
* personalities: id - personalityname - visible (0/1)
* species: id - speciesname - visible (0/1)
* characters: id - charactername - speciesid - personalityid - outfitid - birth (date) - visible (0/1)
* islands: id - islandname - userid - visible (0/1)
* characteronisland: islandid - characterid - outfitid - visible (0/1)


## Known problems
* Ability to remove characters/personalities/species/outfits for admins is not yet possible.
* Certain actions currently redirect to the wrong page due to the correct page requiring a variable, such as the id of an island.
* Some error messages are still plain-looking and need to be changed.
* Issues with sessiontext (which is used as an error message if the user fails to log in or register successfully). This variable will eventually be replaced with something else.
* Animal's page only lists island names, which can cause confusion if multiple users have created an island with the same name.
