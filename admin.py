
from flask import redirect, render_template, request, session
from db import db
from app import app


@app.route("/admin")
def admin():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
        sql = "SELECT personalityname FROM personalities WHERE visible=1"
        result = db.session.execute(sql)
        personalities = result.fetchall()
        sql = "SELECT speciesname FROM species WHERE visible=1"
        result = db.session.execute(sql)
        species = result.fetchall()
        sql = "SELECT outfitname FROM outfits WHERE visible=1"
        result = db.session.execute(sql)
        outfits = result.fetchall()
        sql = "SELECT charactername, id FROM characters WHERE visible=1"
        result = db.session.execute(sql)
        characters = result.fetchall()
        return render_template("admin.html", personalities=personalities, species=species, outfits=outfits, characters=characters)
    else:
        return "You don't have permission."

@app.route("/personalities")
def personalities():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
        sql = "SELECT personalityname FROM personalities WHERE visible=1"
        result = db.session.execute(sql)
        personalities = result.fetchall()
        return render_template("personalities.html", personalities=personalities)
    else:
        return "You don't have permission."

@app.route("/addpersonality",methods=["POST"])
def addpersonality():
    personality = request.form["personality"]
    sql = "SELECT personalityname FROM personalities WHERE personalityname=:personality"
    result = db.session.execute(sql, {"personality":personality})
    checkpersonality = result.fetchone()
    if checkpersonality == None:
        sql = "INSERT INTO personalities (personalityname, visible) VALUES (:personality, 1)"
        db.session.execute(sql, {"personality":personality})
        db.session.commit()   
        return redirect("/personalities")
    else:
        return "A personality with this name already exists."

@app.route("/editpersonality", methods=["POST"])
def editpersonality():
    personality = request.form["old"]
    new = request.form["new"]
    sql = "SELECT personalityname FROM personalities WHERE personalityname=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkpersonality = result.fetchone()
    if checkpersonality == None:
        sql = "SELECT id FROM personalities WHERE personalityname=:personality"
        result = db.session.execute(sql, {"personality":personality})
        id = result.fetchone()[0]
        sql = "UPDATE personalities SET personalityname=:new WHERE id=:id"
        db.session.execute(sql, {"new":new, "id":id})
        db.session.commit()
        return redirect("/personalities")
    else:
        return "A personality with this name already exists."

@app.route("/species")
def species():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
        sql = "SELECT speciesname FROM species WHERE visible=1"
        result = db.session.execute(sql)
        species = result.fetchall()
        return render_template("species.html", species=species)
    else:
        return "You don't have permission."

@app.route("/addspecies",methods=["POST"])
def addspecies():
    species = request.form["species"]
    sql = "SELECT speciesname FROM species WHERE speciesname=:species"
    result = db.session.execute(sql, {"species":species})
    checkspecies = result.fetchone()
    if checkspecies == None:
        sql = "INSERT INTO species (speciesname, visible) VALUES (:species, 1)"
        db.session.execute(sql, {"species":species})
        db.session.commit()   
        return redirect("/species")
    else:
        return "A species with this name already exists."

@app.route("/editspecies", methods=["POST"])
def editspecies():
    species = request.form["old"]
    new = request.form["new"]
    sql = "SELECT speciesname FROM species WHERE speciesname=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkspecies = result.fetchone()
    if checkspecies == None:
        sql = "SELECT id FROM species WHERE speciesname=:species"
        result = db.session.execute(sql, {"species":species})
        id = result.fetchone()[0]
        sql = "UPDATE species SET speciesname=:new WHERE id=:id"
        db.session.execute(sql, {"new":new, "id":id})
        db.session.commit()
        return redirect("/species")
    else:
        return "A species with this name already exists."

@app.route("/outfits")
def outfits():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
        sql = "SELECT outfitname FROM outfits WHERE visible=1"
        result = db.session.execute(sql)
        outfits = result.fetchall()
        return render_template("outfits.html", outfits=outfits)
    else:
        return "You don't have permission."

@app.route("/addoutfit",methods=["POST"])
def addoutfit():
    outfit = request.form["outfit"]
    sql = "SELECT outfitname FROM outfits WHERE outfitname=:outfit"
    result = db.session.execute(sql, {"outfit":outfit})
    checkoutfit = result.fetchone()
    if checkoutfit == None:
        sql = "INSERT INTO outfits (outfitname, visible) VALUES (:outfit, 1)"
        db.session.execute(sql, {"outfit":outfit})
        db.session.commit()   
        return redirect("/outfits")
    else:
        return "An outfit with this name already exists."

@app.route("/editoutfit", methods=["POST"])
def editoutfit():
    outfit = request.form["old"]
    new = request.form["new"]
    sql = "SELECT outfitname FROM outfits WHERE outfitname=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkoutfit = result.fetchone()
    if checkoutfit == None:
        sql = "SELECT id FROM outfits WHERE outfitname=:outfit"
        result = db.session.execute(sql, {"outfit":outfit})
        id = result.fetchone()[0]
        sql = "UPDATE outfits SET outfitname=:new WHERE id=:id"
        db.session.execute(sql, {"new":new, "id":id})
        db.session.commit()
        return redirect("/outfits")
    else:
        return "An outfit with this name already exists."

@app.route("/editcharacter/<int:id>")
def editcharacter(id):
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
        characterid = id
        sql = "SELECT charactername FROM characters WHERE id=:characterid"
        result = db.session.execute(sql, {"characterid":characterid})
        character = result.fetchone()[0]
        #personality
        sql = "SELECT personalityid FROM characters WHERE id=:characterid"
        result = db.session.execute(sql, {"characterid":characterid})
        personalityid = result.fetchone()[0]
        sql = "SELECT personalityname FROM personalities WHERE id=:personalityid"
        result = db.session.execute(sql, {"personalityid":personalityid})
        personality = result.fetchone()[0]
        sql = "SELECT personalityname FROM personalities WHERE visible=1"
        result = db.session.execute(sql)
        personalitylist = result.fetchall()
        #species
        sql = "SELECT speciesid FROM characters WHERE id=:characterid"
        result = db.session.execute(sql, {"characterid":characterid})
        speciesid = result.fetchone()[0]
        sql = "SELECT speciesname FROM species WHERE id=:speciesid"
        result = db.session.execute(sql, {"speciesid":speciesid})
        species = result.fetchone()[0]
        sql = "SELECT speciesname FROM species WHERE visible=1"
        result = db.session.execute(sql)
        specieslist = result.fetchall()
        #defaultoutfit
        sql = "SELECT outfitid FROM characters WHERE id=:characterid"
        result = db.session.execute(sql, {"characterid":characterid})
        outfitid = result.fetchone()[0]
        sql = "SELECT outfitname FROM outfits WHERE id=:outfitid"
        result = db.session.execute(sql, {"outfitid":outfitid})
        outfit = result.fetchone()[0]
        sql = "SELECT outfitname FROM outfits WHERE visible=1"
        result = db.session.execute(sql)
        outfitlist = result.fetchall()
        return render_template("editcharacter.html", characterid=characterid, character=character, personality=personality, personalitylist=personalitylist, species=species, specieslist=specieslist, outfit = outfit, outfitlist = outfitlist)
    else:
        return "You don't have permission."

@app.route("/editcharactername", methods=["POST"])
def editcharactername():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT charactername FROM characters WHERE charactername=:new AND visible=1"
    result = db.session.execute(sql, {"new":new})
    checkname = result.fetchone()
    if checkname == None:
        sql = "UPDATE characters SET charactername=:new WHERE id=:id"
        db.session.execute(sql, {"new":new, "id":id})
        db.session.commit()
        return redirect("/admin")
    else:
        return "A character with this name already exists."

@app.route("/changecharacterspecies", methods=["POST"])
def changecharacterspecies():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT id FROM species WHERE speciesname=:new"
    result = db.session.execute(sql, {"new":new})
    speciesid = result.fetchone()[0]
    sql = "UPDATE characters SET speciesid=:speciesid WHERE id=:id"
    db.session.execute(sql, {"speciesid":speciesid, "id":id})
    db.session.commit()
    return redirect("/admin")

@app.route("/changecharacterpersonality", methods=["POST"])
def changecharacterpersonality():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT id FROM personalities WHERE personalityname=:new"
    result = db.session.execute(sql, {"new":new})
    personalityid = result.fetchone()[0]
    sql = "UPDATE characters SET personalityid=:personalityid WHERE id=:id"
    db.session.execute(sql, {"personalityid":personalityid, "id":id})
    db.session.commit()
    return redirect("/admin")

@app.route("/changecharacteroutfit", methods=["POST"])
def changecharacteroutfit():
    id = request.form["id"]
    new = request.form["new"]
    sql = "SELECT id FROM outfits WHERE outfitname=:new"
    result = db.session.execute(sql, {"new":new})
    outfitid = result.fetchone()[0]
    sql = "UPDATE characters SET outfitid=:outfitid WHERE id=:id"
    db.session.execute(sql, {"outfitid":outfitid, "id":id})
    db.session.commit()
    return redirect("/admin")

@app.route("/addcharacter")
def addcharacter():
    userid = session["userid"]
    sql = "SELECT role FROM users WHERE id=:userid AND visible=1"
    result = db.session.execute(sql, {"userid":userid})
    role = result.fetchone()[0]
    if role == "admin":
        #personality
        sql = "SELECT personalityname FROM personalities WHERE visible=1"
        result = db.session.execute(sql)
        personalities = result.fetchall()
        #species
        sql = "SELECT speciesname FROM species WHERE visible=1"
        result = db.session.execute(sql)
        species = result.fetchall()
        #defaultoutfit
        sql = "SELECT outfitname FROM outfits WHERE visible=1"
        result = db.session.execute(sql)
        outfits = result.fetchall()
        return render_template("addcharacter.html", personalities=personalities, species=species, outfits = outfits)
    else:
        return "You don't have permission."

@app.route("/createcharacter", methods=["POST"])
def createcharacter():
    name = request.form["name"]
    personality = request.form["personality"]
    species = request.form["species"]
    outfit = request.form["outfit"]
    birthday = 101
    sql = "SELECT charactername FROM characters WHERE charactername=:name"
    result = db.session.execute(sql, {"name":name})
    checkcharacter = result.fetchone()
    if checkcharacter == None:
        #personality
        sql = "SELECT id FROM personalities WHERE personalityname=:personality"
        result = db.session.execute(sql, {"personality":personality})
        personalityid = result.fetchone()[0]
        #species
        sql = "SELECT id FROM species WHERE speciesname=:species"
        result = db.session.execute(sql, {"species":species})
        speciesid = result.fetchone()[0]
        #defaultoutfit
        sql = "SELECT id FROM outfits WHERE outfitname=:outfit"
        result = db.session.execute(sql, {"outfit":outfit})
        outfitid = result.fetchone()[0]
        sql = "INSERT INTO characters (charactername, personalityid, speciesid, outfitid, birthmmdd, visible) VALUES (:name, :personalityid, :speciesid, :outfitid, :birthday, 1)"
        db.session.execute(sql, {"name":name, "personalityid":personalityid, "speciesid":speciesid, "outfitid":outfitid, "birthday":birthday})
        db.session.commit()   
        return redirect("/admin")
    else:
        return "A character with this name already exists."
