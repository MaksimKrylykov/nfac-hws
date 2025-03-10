from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Car:
    def __init__(self, id: int, name: str, year: str):
        self.id = id
        self.name = name
        self.year = year


class User:
    def __init__(self, id: int, email: str, first_name: str, last_name: str, username: str):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


cars = [Car(i, "Ford Taurus", str(1926 + i)) for i in range(0, 100)]
users = [User(i, f"test{i}@gmail.com", "Aibek", "Bekturov", f"deadly_knight{i + 95}") for i in range(0, 50)]


@app.get('/cars')
def get_cars(request: Request, response: Response, page: int = 1, limit: int = 10):
    page = int(page)
    if page < 0:
        response.status_code = 400
        return "Invalid page number"
    limit = int(limit)
    if limit < 0:
        response.status_code = 400
        return "Invalid limit number"
    return cars[(page - 1) * limit : page * limit]
    

@app.get('/cars/{id}')
def get_car_by_id(request: Request, response: Response, id: int):
    try:
        return cars[id]
    except:
        response.status_code = 404
        return "Not found"


@app.get('/users')
def get_users(request: Request, response: Response):
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users
        }
    )


@app.get('/users/{user_id}')
def get_user_by_id(request: Request, response: Response, user_id: int):
    try:
        return templates.TemplateResponse(
            "index2.html", {
                "request": request,
                "user": users[user_id]
            }
        )
    except:
        response.status_code = 404
        return "Not found"
