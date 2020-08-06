CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, role TEXT, visible INTEGER);
CREATE TABLE islands (id SERIAL PRIMARY KEY, islandname TEXT, userid INTEGER, visible INTEGER);
CREATE TABLE outfits (id SERIAL PRIMARY KEY, outfitname TEXT, visible INTEGER);
CREATE TABLE species (id SERIAL PRIMARY KEY, speciesname TEXT, visible INTEGER);
CREATE TABLE personalities (id SERIAL PRIMARY KEY, personalityname TEXT, visible INTEGER);
CREATE TABLE characters (id SERIAL PRIMARY KEY, charactername TEXT, speciesid INTEGER, personalityid INTEGER, outfitid INTEGER,  birthmmdd INTEGER, visible INTEGER);
CREATE TABLE characteronisland (islandid INTEGER, characterid INTEGER, outfitid INTEGER, visible INTEGER);
