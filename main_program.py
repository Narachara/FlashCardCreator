#!/usr/bin/python3

from database_functions import *
import uuid
import create_files
import database_functions

def checkforTables():
        isTableCreated = checkIfTablesExist()
        no_cards = checkIfCardIsNotEmpty()
        if no_cards == False:
            print("You have no cards to learn")

        if isTableCreated == False:
            createDatabase()
            print("Tables created")
        
        return no_cards

def choice1():
    card_id  = str(uuid.uuid4())

    frage = create_files.choiceMaker("question")
    antwort = create_files.choiceMaker("answer")

    createCard(card_id, frage, antwort)
    print("Card created \n")
    print("these are the available tags: \n")
    getAllTags()
    
    tags_added = False  # Initialize a flag to False

    while True:
        print("Do you want to add a tag? (y/n)")
        choice = input()

        if choice == "y":
            tag_name = input("Tag name: ")
            strength = input("Strength in numbers 1-9: ")
            if not tag_name:
                print('invalid tag name. \n')
            else:
                addTag(str(uuid.uuid4()), tag_name, card_id, strength)
                print("Tag added \n")
                tags_added = True
        elif tags_added and choice == "n":  # If tags have been added and the user says he doesn't want to add more
            break
        elif not choice:  # Check if the input is an empty string (user pressed Enter)
            print("Error: You must enter 'y' or 'n'. \n")
        else:
            print("Error: You must add at least one tag. \n")

def choice2():
    print("\nThese are the available tags. You must select at least one.\n")
    all_tags_tuples = getAllTags()
    # Extract the strings from the tuples and create a list
    all_tags = [tag[0] for tag in all_tags_tuples]
    topics = []
    i_or_e = None

    while True:
        if i_or_e == None:
            while True:
                i_or_e = input("Do you want to learn exclusively or inclusively? (e/i) \n")
                if i_or_e != "e" and i_or_e != "i":
                    print("Invalid choice. Please enter 'e' or 'i'. \n")                   
                else:
                    break
        topic = input("Which topic do you want to learn? \n")
        if topic and topic in all_tags:
            topics.append(topic)
        elif choice != "y":
            print("Invalid choice. Please enter 'y' or 'n'. \n")
        else:
            print("Please enter a valid topic. \n")

        print("Your learning topics are {0}".format(topics))

        choice  = input("Are these all topics you want? If yes press y \n")
        if choice == "y":
            break

    # Convert the list to a tuple if needed
    topics = tuple(topics)

    # Learn the cards until the user wants to stop
    while True:
        getCardWithSpecificTag(topics, i_or_e)
        choice = input("Do you want to continue? (y/n) \n")
        if choice == "n":
            break

def choice4():
    print("these are the available tags: \n")
    getAllTags()
    tag_name = input("Tag name: ")
    database_functions.getCountofCards_forTag(tag_name)

def choice6():
    database_functions.getCard()


def main():
    while True:# main loop
        print("\n")
        print("1. Create Card")
        print("2. Start Learning")
        print("3. Show all Tags")
        print("4. Show number of cards for tag")
        print("5. Show number of cards")
        print("6. Learn withouth tags")
        print("7. exit")

        no_cards = checkforTables()
        choice = input("What do you want to do? \n")

        if choice == "1":
            choice1()
        elif choice == "2" and no_cards == True:
            choice2()
        elif choice == "3":
            getAllTags()
        elif choice == "5":
            database_functions.getNumberOfCards()
        elif choice == "4":
            choice4()
        elif choice == "6":
            choice6()



        if choice == "7":
            print("keep learning")
            print("Goodbye")
            break
                    

if __name__ == "__main__":
    main()
