import sqlite3
import feedparser
import json


def create_db():
    try:
        con = sqlite3.connect("./rss.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS news(title, link type UNIQUE, new)")
        con.commit()
        return "base de datos creada"
    except:
        return "la base de datos ya existe"


def add_item_to_db(title, link, new):
    try:
        con = sqlite3.connect("./rss.db")
        cur = con.cursor()
        
        cur.execute(f"""
            INSERT or IGNORE INTO news VALUES
            ('{title.replace("'","''").replace('"',"''")}',
            '{link}',
            {new})""")

        con.commit()
    except:
        create_db()

def new_entries_db():
    """return a list with db entries marked as new=True"""
    con = sqlite3.connect("./rss.db")
    cur = con.cursor()

    try:
        res = cur.execute("SELECT title, link from news WHERE new=True")

        return [{"title":i[0], "link":i[1]} for i in res]
    except:
        return []

def update_entry(link):
    con = sqlite3.connect("./rss.db")
    cur = con.cursor()

    cur.execute(f"UPDATE news SET new=False WHERE link='{link}'")

    con.commit()


def parse_and_upload_to_db(rss_list, status=True):
    # parse a list of rss and upload every entry to the database
    for rss in rss_list:
        d = feedparser.parse(rss)

        for entry in d.entries:
            add_item_to_db(entry.title, entry.link, status)


def add_suscription(rss):
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)

        if rss not in data["suscripciones"]:
            data["suscripciones"].append(rss)

            with open("settings.json", "w") as file:
                json.dump(data, file, indent=4)

            return "suscripcion agregada"

        return "la suscripcion ya existe"

    except FileNotFoundError:
        with open("settings.json", "w") as file:
            json.dump(
                {"suscripciones":[rss]},
                file,
                indent=4)

        return "suscripcion agregada"

def remove_suscription(index):
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)
        
        # a este try lo deberia escribir mejor
        try:
            deleted = data["suscripciones"].pop(index)

            with open("settings.json", "w") as file:
                json.dump(data, file, indent=4)
            
            return f"suscripcion a '{deleted}' eliminada"

        except:
            return "la suscripcion no existe"
    
    except:
        return "no tenes ninguna suscripcion"

def list_suscriptions():
    """return a list with the suscriptions"""
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)
        
        return data["suscripciones"]

    except FileNotFoundError:
        return []


def valid_rss(rss):
    d = feedparser.parse(rss)

    if d.feed.get('title'):
        return True
    
    return False




