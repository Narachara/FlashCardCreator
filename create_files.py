import pathlib as pl
import subprocess
import uuid
import os


def open_file(subfolder, filetype):
    filename = str(uuid.uuid4()) + "." + filetype
    file_path = os.path.join(subfolder, filename)

    os.makedirs(subfolder, exist_ok=True)

    with open(file_path, 'w') as file:
        pass  # Create an empty file

    subprocess.Popen(["subl", file_path])
    print(f"created file: {file_path}")
    return file_path


def list_all_dirs():
    return [x for x in pl.Path().iterdir() if x.is_dir()]


def menu():
        print("1. Text")
        print("2. Markdown")
        print("3. Python")
        print("4. Bash")
        print("5. C")
        print("6. C++")
        print("7. link to a website")
        print("8. folder")
        print("9. Jupyter Notebook ")
        print("10. Commandline Card \n")


def choiceMaker(card_side):
        menu()
        choice = input(f"What type of card do you want to create for the {card_side}? \n")

        if choice == "1":
            filetype = "txt"
        elif choice == "2":
            filetype = "md"
        elif choice == "3":
            filetype = "py"
        elif choice == "4":
            filetype = "sh"
        elif choice == "5":
            filetype = "c"
        elif choice == "6":
            filetype = "cpp"
        elif choice == "7":
            card_side = input("Link: ")
            subfolderName = "links"
        elif choice == "8":
            foldername = input("Folder name: ")
        elif choice == "9":
             filetype = "ipynb"
        elif choice == "10":
             frage = input("TEXT: ")
             card_side = 'FRAGE: ' + frage
             return card_side
        else:
            raise ValueError("invalid choice")
        
        
        if choice == "8":
            print("theses are already existing folders: \n")
            print(list_all_dirs())
            subfolderName = input("Parent folder name: ")
            fullpath = os.path.join(subfolderName,foldername)
            os.makedirs(fullpath)
            card_side = fullpath
            #open folder in file manager
            subprocess.Popen(["xdg-open", str(fullpath)])
        

        if choice != "7" and choice != "8":
            print("theses are already existing folders: \n")
            print(list_all_dirs())
            subfolderName = input("Parentfolder name: ")
            question_file = open_file(subfolderName, filetype)
            card_side = question_file
            
        return card_side