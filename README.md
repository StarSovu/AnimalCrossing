# AnimalCrossing
tsoha 2020


Application for users to create their own island and select Animal Crossing characters for their island.

Each user has a username (unique) and password. Users can also name their island, which is different from the username and not necessarily unique. Each user can only have one island, and each island can have a maximum of 10 animals.

Only a user with admin rights can create and edit characters. All users can select and change characters for their own island. If the island is full and the user tries to add another character, they will get a message saying that they need to kick someone off their island before they can add another character. Users cannot have the same character multiple times, but multiple users can have the same character on their island.

Characters have: name (unique), birthday (month and day), species and personality.
Personalities: Normal, Peppy, Snooty, Sisterly, Lazy, Cranky, Jock, Smug

Any visitor can see the list of charactes and filter it by species and/or personality. Lists can be arranged alphabetically or by birthday. There is also a search function, which allows visitors to search for characters with specific names. Visitors can see for which islands each character is selected to.

Optional, after other features of the application have been compeleted:
There are also outfits, which users can give to animals on their island. Each animal has a specific default outfit which they wear if the user does not change them. Each animal can only wear one outfit, but the same outfit can be given to multiple animals. If the same animal is on multiple islands, they can have different outfit on different islands, so users cannot change animals' outfits on other islands.


Application utlizes a database. In database there are tables:

Users
Username - Password hash value - Rights(user/admin) - Visible (0/1)

Outfits
Id - Outfit name - Visible (0/1)

Personalities
Id - Personality - Visible (0/1)

Species
Id - Species - Visible (0/1)

Characters
Character name - Species id - Birthday (MM/DD) - Personality id - Outfit id - Visible (0/1)

Islands
Island name - User id - Character id - Outfit id - Visible (0/1)
