import sqlite3
import subprocess
import uuid
import os
import sys


con = sqlite3.connect("learn.db")
cur = con.cursor()


def checkIfTablesExist():
    cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='card'""")
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False


def checkIfCardIsNotEmpty():
    cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='card'""")
    if cur.fetchone()[0] == 1:
        cur.execute("""SELECT count(*) FROM card""")
        if cur.fetchone()[0] == 0:
            return False
        else:
            return True
    else:
        return False


def createDatabase():
    createcardTable()
    createTagTable()


def createcardTable():
    cur.execute("""
        CREATE TABLE card(
        id UUID DEFAULT '{}',
        frage VARCHAR,
        antwort VARCHAR,
        score INT,
        PRIMARY KEY(id)
        );
    """.format(str(uuid.uuid4())))


def createTagTable():
    cur.execute("""
        CREATE TABLE tag(
        id UUID DEFAULT '{}',
        name VARCHAR,
        card_id INTEGER NOT NULL,
        strength INT,
        PRIMARY KEY(id),
        CONSTRAINT card_tag FOREIGN KEY (card_id) REFERENCES card (id)
        );
    """.format(str(uuid.uuid4())))


def createCard(card_id, frage, antwort):
    cur.execute("""
    INSERT INTO card (id, frage, antwort, score) VALUES
        (?, ?, ?, ?)
    """, (card_id, frage, antwort, 0))
    con.commit()


def addTag(id, name, card_id, strength):
    cur.execute("""
    INSERT INTO tag (id, name, card_id, strength) VALUES
        (?, ?, ?,?)
    """, (id, name, card_id, strength))
    con.commit()


def getQuestionOfCard(card_id):
    res = cur.execute("SELECT frage FROM card where id = ?",(card_id,))
    frage = res.fetchone()
    if os.name == 'nt':
        if frage[0].startswith("http") or frage[0].startswith("www"):
            subprocess.Popen(["brave-browser", frage[0]])
        else:
            os.startfile(frage[0])
    else:
        if frage[0].startswith("http") or frage[0].startswith("www"):
            subprocess.Popen(["brave-browser", frage[0]])
        elif frage[0].startswith("FRAGE: "):
            print(frage[0].replace("FRAGE: ", ""), "\n")
        else:
            subprocess.call(['xdg-open', frage[0]])    


def getAnswerOfCard(card_id):
    res = cur.execute("SELECT antwort FROM card where id = ?",(card_id,))
    answer = res.fetchone()

    if os.name == 'nt':
        if answer[0].startswith("http") or answer[0].startswith("www"):
            subprocess.Popen(["brave-browser", answer[0]])
        else:
            os.startfile(answer[0])
    elif answer[0].startswith("FRAGE: "):
        print(answer[0].replace("FRAGE: ", ""), "\n")
    else:
        if answer[0].startswith("http") or answer[0].startswith("www"):
            subprocess.Popen(["brave-browser", answer[0]])
        else:
            subprocess.call(['xdg-open', answer[0]])


def getTagsOfCard(card_id):
    res = cur.execute("SELECT name from tag WHERE card_id = ?",(card_id,))
    antwort = res.fetchall()
    print(antwort)


def getProgressOfCard(card_id):
    res = cur.execute("SELECT score FROM card where id = ?",(card_id,))
    id = res.fetchone()
    return id[0]


def updateProgress(card_id):
    cur.execute("""
    UPDATE card SET score = score + 1 WHERE id = ?;
    """, (card_id,))
    con.commit()


def deleteProgressFromCard(card_id):
    cur.execute("""
    UPDATE card SET score = 0 WHERE id = ?;
    """, (card_id,))
    con.commit()


def deleteCard(card_id):
    res = cur.execute("SELECT frage FROM card where id = ?",(card_id,))
    frage = res.fetchone()
    if os.name == 'nt':
        if frage[0].startswith("http") or frage[0].startswith("www"):
            pass
        else:
            os.remove(frage[0])
    #for linux
    else:
        if frage[0].startswith("http") or frage[0].startswith("www"):
            pass
        elif frage[0].startswith("FRAGE: "):
            pass
        else:
            os.remove(frage[0])
    
    res = cur.execute("SELECT antwort FROM card where id = ?",(card_id,))
    antwort = res.fetchone()
    if os.name == 'nt':
        if antwort[0].startswith("http") or antwort[0].startswith("www"):
            pass
        else:
            os.remove(antwort[0])
    #for linux
    else:
        if antwort[0].startswith("http") or antwort[0].startswith("www"):
            pass
        elif antwort[0].startswith("FRAGE: "):
            pass
        else:
            os.remove(antwort[0])
    cur.execute("DELETE FROM tag WHERE card_id = ?", (card_id,))
    cur.execute("DELETE FROM card WHERE id = ?", (card_id,))
    con.commit()
    print(f"Deleted card {card_id}")
    print("\n")


def deleteTag(tag_name, card_id):
    try:
        # Check if the card has more than one tag before deleting
        cur.execute("SELECT COUNT(*) FROM tag WHERE card_id = ?", (card_id,))
        tag_count = cur.fetchone()[0]
        
        if tag_count > 1:
            cur.execute("DELETE FROM tag WHERE name = ? AND card_id = ?", (tag_name, card_id))
            con.commit()
            print(f"Deleted tag '{tag_name}' from card {card_id}")
        else:
            print(f"Card {card_id} must have at least one tag. Cannot delete the last tag.")
    except sqlite3.Error as e:
        print("SQLite Error:", e)
        con.rollback()  # Roll back the transaction if an error occurs
        # Handle the error or perform any necessary cleanup here
    except Exception as e:
        print("Error:", e)
        # Handle other exceptions here


def getAllTags():
    res = cur.execute("SELECT DISTINCT(name) from tag")
    tags = res.fetchall()

    num_tags = len(tags)
    num_per_row = 8

    print("\n")

    for i in range(0, num_tags, num_per_row):
        row_tags = tags[i:i+num_per_row]
        print(' '.join(tag[0] for tag in row_tags))
    print("\n")
    
    return tags


def getCountofCards_forTag(tag):
    query = """
        SELECT COUNT(*)
        FROM card c
        INNER JOIN tag t ON c.id = t.card_id
        WHERE t.name = ?
    """
    res = cur.execute(query, (tag,))
    count = res.fetchone()[0]
    print(f"Number of cards for tag '{tag}': {count}")
    return count


def getNumberOfCards():
    res = cur.execute("SELECT COUNT(*) FROM card")
    count = res.fetchone()[0]
    print(f"Number of cards: {count}")
    return count


def exclusiveQuery(tags):
    card_id = None
    placeholders = ', '.join(['?'] * len(tags))

    query = f"""
        SELECT c.id
        FROM card c 
        INNER JOIN tag t ON c.id = t.card_id
        WHERE t.name IN ({placeholders})
        GROUP BY c.id
        HAVING COUNT(DISTINCT t.name) = {len(tags)}
        ORDER BY c.score
        LIMIT 1;
    """
    
    res = cur.execute(query, tags)
    card = res.fetchone()

    if card is not None:
        card_id = card[0]
    else:
        print("No card found for the given tags.")
        sys.exit(1)


    return card_id


def inclusiveQuery(tags):
    # Generate placeholders for the tags based on the length of the tuple
    placeholders = ', '.join(['?'] * len(tags))
    card_id = None
    # Modify the SQL query to use the placeholders
    query = f"""
        SELECT DISTINCT c.*
        FROM card c 
        INNER JOIN tag t ON c.id = t.card_id
        WHERE t.name IN ({placeholders})
        ORDER BY c.score
        LIMIT 1;
    """

    
    res = cur.execute(query, tags)
    card = res.fetchone()
    card_id = card[0]

    if card is not None:
        card_id = card[0]
    else:
        print("No card found for the given tags.")
        sys.exit(1)


    return card_id


def programFlow(card_id):
    getQuestionOfCard(card_id)

    print("the progress of the card is: ", getProgressOfCard(card_id))
    print("Do you want to see the answer? (y/n) \n")
    choice = input()
    if choice == "y":
        getAnswerOfCard(card_id)

    print("Do you want to see the tags of the card? (y/n) \n")
    choice = input()
    if choice == "y":
        getTagsOfCard(card_id)

    print("Do you want to add a tag? (y/n) \n")
    choice = input()
    if choice == "y":
        print("these are tags of the card: \n")
        getAllTags()
        while True:
            tag_name = input("Tag name: ")
            strength = input("Strength in numbers 1-9: ")
            addTag(str(uuid.uuid4()), tag_name, card_id, strength)
            print("Tag added")
            print("Do you want to add another tag? (y/n) \n")

            choice = input()
            if choice == "n":
                break

    print("Do want to delete a tag? (y/n)\n")
    choice = input()

    if choice == "y":
        while True:
            tag_name = input("Tag name: ")
            deleteTag(tag_name, card_id)
            print("Do you want to delete another tag? (y/n)")
            choice = input()
            if choice == "n":
                break

    print("Do you want to delete the progress? (y/n)")
    choice = input()
    if choice == "y":
        deleteProgressFromCard(card_id)

    print("Did you know the answer? (y/n)")
    choice = input()
    if choice == "y":
        updateProgress(card_id)

    print("Do you want to delete the card? (y/n)")
    choice = input()
    if choice == "y":
        deleteCard(card_id)


def getCardWithSpecificTag(tags, e_or_i):
    choice = e_or_i
    card_id = None
    if choice == "e":
        card_id = exclusiveQuery(tags)

    elif choice == "i":
        card_id = inclusiveQuery(tags)
    else:
        # error
        print("Error: You must enter 'e' or 'i'. \n")

    programFlow(card_id)


def getCard():
    query = f"""
        SELECT id FROM card
        ORDER BY score
        LIMIT 1;
    """

    res = cur.execute(query)
    card = res.fetchone()
    card_id = card[0]

    programFlow(card_id)