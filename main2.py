from fastapi import FastAPI, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn


app = FastAPI()

class BOOK:
    book_id = int
    book_name = str
    author_name = str
    description = str
    rating = float

    def __init__(self, book_id, book_name, author_name, description, rating):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.description = description
        self.rating = rating
    
class BookRequest(BaseModel):
    book_id: Optional[int] = Field(description='book_id is not neded on create')
    book_name: str = Field(min_length=3, max_length=100)
    author_name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=200)
    rating: float = Field(ge=0, le=6)

model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "Fikre Miko",
                "description": "The new era of coding",
                "rating": 3
                }
            }
        }

books = [
    BOOK(1, "Mike and sytems", "Miko", "the best book to learn systems", 5),
    BOOK(2, "The live of API", "Fikre", "What you need to master API", 4.5),
    BOOK(3, "Fast with FastAPI", "Lio", "Code faster code smarter", 4.2),
    BOOK(4, "Nteworking and HTTP", "Jack Ma", "How to manage HTTP", 3.4),
    BOOK(5, "Python and use", "Fikre", "The way to master python", 4.2),
    BOOK(6, "Live death and robote", "Lio", "Learn how to countrol Hardware", 5)
]
@app.get("/")
def welcome():
    return {"message: Welcome to the book store"}

@app.get("/books")
def list_books():
    return books

@app.get("/book/{book_book_id}")
def return_book_book_id(book_book_id: int = Path(gt=0)):
    for book in books:
        if book.book_id == book_book_id:
            return book

@app.get("/book/")
def return_rating(book_rating: float = Path(gt=0)):
    book_list = []
    for book in books:
        if book.rating == book_rating:
            book_list.append(book)
    return book_list

@app.post("/book")
def create_book(book: BookRequest):
    if len(books) > 0:
        book.book_id = books[-1].book_id + 1
    else:
        book.book_id = 1
    return book

@app.post("/create_new_book")
def create_new_book(book: BookRequest):
    new_book = BOOK(**book.model_dump())
    books.append(new_book)
    return new_book

@app.put("/book/book_update")
def book_update(book: BookRequest):
    for i in range(len(books)):
        if books[i].book_id == book.book_id:
            books[i] = book
            return {"message": "Book updated successfully!"}
    return {"message": "Book not found!"}

@app.delete("/books/{book_id}")
def delete_book(bookid: int = Path(gt=0, le=len(books))):
    for i in range(len(books)):
        if books[i].book_id == bookid:
            books.pop(i)
            return {"message": "Book deleted successfully!"}
    return {"message": "book not found!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)