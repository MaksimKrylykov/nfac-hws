from fastapi import FastAPI, Request, Response, Form, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from jose import jwt
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class User:
    def __init__(self, id: int, email: str, name: str, password: str):
        self.id = id
        self.email = email
        self.name = name
        self.password = password
    

class UserRepository:
    def __init__(self):
        self.users = [User(1, '1', '1', '1')]
        self.curId = 2
    
    def add_user(self, user: User):
        user.id = self.curId
        self.curId += 1
        self.users.append(user)
    
    def get_user_by_id(self, id: int):
        for user in self.users:
            if user.id == id:
                return user
        return None
    
    def get_user_by_email(self, email: str):
        for user in self.users:
            if user.email == email:
                return user
        return None


class Flower:
    def __init__(self, id: int, name: str, quantity: int, price: float):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price


class FlowerRepository:
    def __init__(self):
        self.flowers = [
            Flower(1, "White flower", 5, 1.99),
            Flower(2, "Red flower", 7, 2.49),
            Flower(3, "Green flower", 10, 1.39),
        ]
        self.curId = 4
    
    def get_all(self):
        return self.flowers
    
    def add_flower(self, flower: Flower):
        flower.id = self.curId
        self.curId += 1
        self.flowers.append(flower)
    
    def get_flower_by_id(self, id: int):
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None


userRep = UserRepository()

flowerRep = FlowerRepository()


def create_jwt(id: int):
    body = {"user_id" : id}
    return jwt.encode(body, "amogus", "HS256")


def decode_jwt(token: str):
    if str == None:
        return -1
    return jwt.decode(token, "amogus", "HS256")["user_id"]


@app.get("/signup")
def get_register(request: Request, response: Response):
    return templates.TemplateResponse(
        "register.html", {
            "request": request
        }
    )


@app.post("/signup")
def post_register(request: Request, response: Response,
                 email = Form(), name = Form(), password = Form()):
    
    user = userRep.get_user_by_email(email)
    if user != None:
        return "Email is already in use!"
    
    user = User(0, email, name, password)
    userRep.add_user(user)
    return RedirectResponse("/login", status_code=303)


@app.get("/login")
def get_login(request: Request, response: Response):
    return templates.TemplateResponse(
        "login.html", {
            "request": request
        }
    )


@app.post("/login")
def post_login(request: Request, response: Response,
                 email = Form(), password = Form()):

    user = userRep.get_user_by_email(email)
    
    if user == None or user.password != password:
        return "Incorrent email or password"

    response = RedirectResponse("/profile", status_code=303)
    response.set_cookie("token", create_jwt(user.id))
    return response


@app.get("/profile")
def get_profile(request: Request, response: Response,
                 token = Cookie(default=None)):
    
    user_id = decode_jwt(token)
    user = userRep.get_user_by_id(user_id)

    if user == None:
        return RedirectResponse("/login", status_code=303)
    
    return templates.TemplateResponse(
        "profile.html", {
            "request": request,
            "user": user
        }
    )


@app.get("/flowers")
def get_flowers(request: Request, response: Response, token = Cookie(default=None)):
    
    user_id = decode_jwt(token)
    user = userRep.get_user_by_id(user_id)

    if user == None:
        return RedirectResponse("/login", status_code=303)

    flowers = flowerRep.get_all()

    return templates.TemplateResponse("flowers.html", {
        "request": request,
        "flowers": flowers
    })


@app.get("/flowers/new")
def get_flowers_form(request: Request, response: Response, token = Cookie(default=None)):
    
    user_id = decode_jwt(token)
    user = userRep.get_user_by_id(user_id)

    if user == None:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse("new.html", {
        "request": request,
    })


@app.post("/flowers/new")
def add_flowers(request: Request, response: Response,
                token = Cookie(default=None), name = Form(), quantity = Form(), price = Form()):
    
    user_id = decode_jwt(token)
    user = userRep.get_user_by_id(user_id)

    if user == None:
        return RedirectResponse("/login", status_code=303)

    flower = Flower(0, name, quantity, float(price))
    flowerRep.add_flower(flower)

    return RedirectResponse("/flowers", status_code=303)


@app.get("/cart/items")
def get_cart(request: Request, response: Response,
                token = Cookie(default=None)):
    user_id = decode_jwt(token)
    user = userRep.get_user_by_id(user_id)

    if user == None:
        return RedirectResponse("/login", status_code=303)
    
    cart_raw = request.cookies.get("cart")
    if cart_raw == None:
        cart_raw = "[]"
    cart = json.loads(cart_raw)

    flowers = []
    total_price = 0
    for id in cart:
        flower = flowerRep.get_flower_by_id(int(id))
        if flower != None:
            flowers.append(flower)
            total_price += flower.price
    
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "flowers": flowers,
        "total_price": f"{total_price:.2f}"
    })


@app.post("/cart/items")
def add_to_cart(request: Request, response: Response, flower_id = Form(),
                token = Cookie(default=None)):
    
    user_id = decode_jwt(token)
    user = userRep.get_user_by_id(user_id)

    if user == None:
        return RedirectResponse("/login", status_code=303)
    
    cart_raw = request.cookies.get("cart")
    if cart_raw == None:
        cart_raw = "[]"
    cart = json.loads(cart_raw)
    
    flower = flowerRep.get_flower_by_id(int(flower_id))

    if flower == None:
        return RedirectResponse("/flowers", status_code=303)
    
    cart.append(flower_id)
    response = RedirectResponse("/flowers", status_code=303)
    response.set_cookie("cart", json.dumps(cart))
    return response

