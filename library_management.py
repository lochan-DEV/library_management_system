import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "library.json"


def main(): 
    x=add_book()
    print(x)
    print("Enter 1 to borrow book :  or  Enter 2 to return book : ")
    choice=int(input("Enter your choice : "))
    try:        
        if choice==1:
            y=question()
            print(y)
        elif choice==2:
            z=return_book()
            print(z)
    except ValueError:
        print("incorrect option entered")
        return
        

def load_books():
    DATA_DIR.mkdir(exist_ok=True)
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []

def save_books(books):
    with open(DATA_FILE, "w") as f:
        json.dump(books, f)

def add_book():
    title = input("Enter title: ")
    author = input("Enter author: ")

    books = load_books()

    for book in books:
        if book["title"] == title:
            return f'This book already exists. Copies available: , {book["available_copies"]}'

    copies = 20
    new_book = {
                          "title": title,
                          "author": author,
                          "total_copies": copies,
                          "available_copies": copies,
                           "borrowers_list":[]
            }
    books.append(new_book)
    save_books(books)
    return f'This book already exists. Copies available: , {new_book["available_copies"]}'


def question():
    books = load_books()
    print("Enter your NAME and DATE")
    title = input("enter the book name you need to borrow : ")
    borrowers_name = input("YOUR NAME : ")
    current_date = input("DATE : ")
    for book in books:
        if book["title"] == title:
            book["borrowers_list"].append({"name": borrowers_name, "date": current_date})
            book["available_copies"] -= 1
    save_books(books)
    return "THANK YOU"




def return_book():
    books=load_books()
    title=input("enter the name of the book : ")
    returners_name=input("enter your name : ")
    present=input("enter the date of return :")
    for book in books:
        if book["title"] == title:
            for entry in book["borrowers_list"]:
                if entry["name"] == returners_name: 
                    due_date = entry["date"]
                    date_format = "%d/%m/%Y"
                    due_date_obj = datetime.strptime(due_date, date_format)
                    present_obj = datetime.strptime(present, date_format)
                    diff = present_obj - due_date_obj
                    days_late = diff.days
                    if days_late>15:
                        penalty=2*days_late
                        book["borrowers_list"].remove(entry)
                        book["available_copies"]+=1
                        save_books(books)
                        return f"you have to pay the penalty of {penalty} ruppees for late submission"
                    else:
                        book["borrowers_list"].remove(entry)
                        book["available_copies"]+=1
                        save_books(books)
                        return "you have returned it in time"   

if __name__ == "__main__":
    main()


