from fastapi import FastAPI, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Comment:

    def __init__(self, id: int, text: str, rating: bool):
        self.text = text
        self.rating = rating


class CommentRepo:

    def __init__(self):
        self.comments = []
        self.curId = 0
    
    def getAll(self):
        return self.comments[::-1]
    
    def get_curId(self):
        return self.curId
    
    def save(self, comment: Comment):
        self.comments.append(comment)
        self.curId += 1
    

repository = CommentRepo()

repository.save(Comment(0, "Test Comment", True))


@app.post("/comments/new")
def post_comments_form(request: Request, response: Response, text: str = Form(), rating: str = Form()):
    comment = Comment(repository.get_curId, text, rating == "positive")
    repository.save(comment)
    return RedirectResponse("/comments", status_code=303)


@app.get("/comments/new")
def get_comments_form(request: Request, response: Response):
    return templates.TemplateResponse(
        "new.html", {
            "request": request
        }
    )


@app.get("/comments")
def get_comments(request: Request, response: Response, page: int = 1, limit: int = 4):

    comments = repository.getAll()

    total_pages = (len(comments) + limit - 1) // limit

    return templates.TemplateResponse("index.html", {
        "request": request,
        "comments": comments[(page - 1) * limit : page * limit],
        "page": page,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1,
        "next_page": page + 1,
        "limit": limit
    })