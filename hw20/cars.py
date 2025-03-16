from fastapi import FastAPI, Request, Response, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Car:
    def __init__(self, id: int, name: str, year: str):
        self.id = id
        self.name = name
        self.year = year


class CarsRepository:
    def __init__(self):
        self.cars = [
            Car(1, "My car", 1885),
            Car(2, "Cat", 2010),
            Car(3, "Car car", 1990),
            Car(4, "Honda", 2015),
            Car(5, "Honda 2", 2016),
            Car(6, "My cat", 2015)
        ]
    
    def get_all(self):
        return self.cars
    
    def get_filtered(self, filter: str):
        return [car for car in self.cars if filter.lower() in car.name.lower()]
    
    def get_nextId(self):
        return len(self.cars) + 1

    def save(self, newCar: Car):
        self.cars.append(newCar)


repository = CarsRepository()

@app.get("/cars")
def search_cars(request: Request):
    cars = repository.get_all()
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "cars": cars
        }
    )

@app.get("/cars/search")
def search_cars(request: Request, q: str = ""):
    filtered_cars = repository.get_filtered(q)
    return templates.TemplateResponse(
        "search.html", {
            "request": request,
            "cars": filtered_cars
        }
    )

@app.get("/cars/new")
def new_car_form(request: Request):
    return templates.TemplateResponse(
        "new.html", {
            "request": request
        }
    )

@app.post("/cars/new")
def post_car(request: Request, response: Response, name: str = Form(), year: str = Form()):
    if not(year.isdigit()):
        response.status_code = 405
        return "Year must be a number"
    car = Car(repository.get_nextId(), name, year)
    repository.save(car)
    return RedirectResponse("/cars", status_code=303)
