CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, role TEXT, visible INTEGER);
CREATE TABLE islands (id SERIAL PRIMARY KEY, islandname TEXT, userid INTEGER, visible INTEGER);
CREATE TABLE outfits (id SERIAL PRIMARY KEY, outfitname TEXT, visible INTEGER);
CREATE TABLE species (id SERIAL PRIMARY KEY, speciesname TEXT, visible INTEGER);
CREATE TABLE personalities (id SERIAL PRIMARY KEY, personalityname TEXT, visible INTEGER);
CREATE TABLE characters (id SERIAL PRIMARY KEY, charactername TEXT, speciesid INTEGER, personalityid INTEGER, outfitid INTEGER, birth DATE, visible INTEGER);
CREATE TABLE characteronisland (islandid INTEGER, characterid INTEGER, outfitid INTEGER, visible INTEGER);
/* Add these only one time!
INSERT INTO personalities (personalityname, visible) VALUES ('Normal', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Peppy', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Snooty', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Sisterly', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Lazy', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Jock', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Cranky', 1);
INSERT INTO personalities (personalityname, visible) VALUES ('Smug', 1);
*/
ALTER TABLE characters ADD CONSTRAINT characters_speciesid_fkey FOREIGN KEY (speciesid) REFERENCES species(id);
ALTER TABLE characters ADD CONSTRAINT characters_personality_fkey FOREIGN KEY (personalityid) REFERENCES personalities(id);
ALTER TABLE characters ADD CONSTRAINT characters_outfitid_fkey FOREIGN KEY (outfitid) REFERENCES outfits(id);
ALTER TABLE characters ALTER COLUMN charactername SET NOT NULL;

ALTER TABLE islands ADD CONSTRAINT islands_userid_fkey FOREIGN KEY (userid) REFERENCES users(id);
ALTER TABLE islands ALTER COLUMN islandname SET NOT NULL;

ALTER TABLE characteronisland ADD CONSTRAINT characteronisland_islandid_fkey FOREIGN KEY (islandid) REFERENCES islands(id);
ALTER TABLE characteronisland ADD CONSTRAINT characteronisland_characterid_fkey FOREIGN KEY (characterid) REFERENCES characters(id);
ALTER TABLE characteronisland ADD CONSTRAINT characteronisland_outfitid_fkey FOREIGN KEY (outfitid) REFERENCES outfits(id);
