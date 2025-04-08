from fastapi import FastAPI, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class Book:
    def __init__(self, id: int, title: str, author: str, year: int, total_pages: int, genre: str):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.total_pages = total_pages
        self.genre = genre


class BooksRepository:
    def __init__(self):
        self.books = [
            Book(i, "Book" + str(i), "Author" + str(i), 1900 + i, 64 + i, "Genre" + str(i)) for i in range(1, 35)
        ]
        self.curId = len(self.books)
    
    def get_all(self):
        return self.books
    
    def get_nextId(self):
        self.curId += 1
        return self.curId
    
    def save(self, book: Book):
        self.books.append(book)
    
    def getByIndex(self, id):
        for book in self.books:
            if book.id == id:
                return book
        return None
    
    def update(self, id, book: Book):
        for i in range(len(self.books)):
            if (self.books[i].id == id):
                self.books[i] = book
                return
    
    def remove(self, id):
        for i in range(len(self.books)):
            if (self.books[i].id == id):
                del self.books[i]
                return


repository = BooksRepository()


@app.post("/books/{id}/delete")
def delete_book(request: Request, id: int):

    repository.remove(id)
    return RedirectResponse("/books", status_code=303)


@app.get("/books/{id}/edit")
def edit_book_form(request: Request, response: Response, id: int):

    book = repository.getByIndex(id)
    if book == None:
        response.status_code = 404
        return "Not found"
    
    return templates.TemplateResponse(
        "upd.html", {
            "request": request,
            "book": book
        }
    )


@app.post("/books/{id}/edit")
def post_book(request: Request, response: Response, id: int, title: str = Form(), author: str = Form(), year: int = Form(), total_pages: int = Form(), genre: str = Form()):

    book = Book(id, title, author, year, total_pages, genre)
    repository.update(id, book)
    return RedirectResponse("/books", status_code=303)


@app.get("/books/new")
def new_book_form(request: Request):
    return templates.TemplateResponse(
        "new.html", {
            "request": request
        }
    )


@app.post("/books/new")
def post_book(request: Request, response: Response, title: str = Form(), author: str = Form(), year: int = Form(), total_pages: int = Form(), genre: str = Form()):

    book = Book(repository.get_nextId(), title, author, year, total_pages, genre)
    repository.save(book)
    return RedirectResponse("/books", status_code=303)


@app.get("/books")
def get_books(request: Request, response: Response, page: int = 1, limit: int = 10):

    books = repository.get_all()
    total_pages = (len(books) + limit - 1) // limit

    return templates.TemplateResponse("index.html", {
        "request": request,
        "books": books[(page - 1) * limit : page * limit],
        "page": page,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
        "limit": limit
    })


@app.get("/books/{id}")
def get_book_by_id(request: Request, response: Response, id: int):

    book = repository.getByIndex(id)

    if book == None:
        response.status_code = 404
        return "Not found"

    return templates.TemplateResponse("book.html", {
        "request": request,
        "book": book
    })