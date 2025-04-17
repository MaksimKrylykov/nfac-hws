from fastapi import FastAPI, Request, Response, HTTPException, status, Form, Cookie, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel, field_validator
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    id: int
    email: str
    name: str
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v
    

class UserRepository:
    def __init__(self):
        self.users = [User(id=1, email='1', name='1', password='12345678')]
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


class Flower(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

    @field_validator("quantity")
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError("Quantity must be non-negative")
        return v
    
    @field_validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v


class FlowerRepository:
    def __init__(self):
        self.flowers = [
            Flower(id=1, name="White flower", quantity=5, price=1.99),
            Flower(id=2, name="Red flower", quantity=7, price=2.49),
            Flower(id=3, name="Green flower", quantity=10, price=1.39),
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
    try:
        return jwt.decode(token, "amogus", "HS256")["user_id"]
    except:
        return None


class SignupData(BaseModel):
    email: str
    name: str
    password: str


@app.post("/signup")
def post_register(user: SignupData):
    if userRep.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already in use")
      
    userRep.add_user(User(id=0, **user.model_dump()))
    return {"message": "User registered"}


@app.post("/login")
def post_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = userRep.get_user_by_email(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_jwt(user.id)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    user = userRep.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class UserInfo(BaseModel):
    email: str
    name: str


@app.get("/profile", response_model=UserInfo)
def get_profile(current_user = Depends(get_current_user)):
    return UserInfo(email=current_user.email, name=current_user.name)


@app.get("/flowers", response_model=list[Flower])
def get_flowers(user = Depends(get_current_user)):
    return flowerRep.get_all()


class FlowerData(BaseModel):
    name: str
    quantity: int
    price: float


@app.post("/flowers")
def add_flowers(flower: FlowerData, user = Depends(get_current_user)):
    new_flower = Flower(id=0, **flower.model_dump())
    flowerRep.add_flower(new_flower)
    return {"message": "Flower added", "flower": new_flower}


class FlowerInfo(BaseModel):
    id: int
    name: str
    price: str

    model_config = {
        "extra": "ignore"
    }


@app.get("/cart/items")
def get_cart(request: Request, user = Depends(get_current_user)):
    cart_json = dict()
    flowers = []
    total_price = 0

    cart_raw = request.cookies.get("cart")
    if cart_raw == None:
        cart_raw = "[]"
    cart = json.loads(cart_raw)

    for id in cart:
        flower = flowerRep.get_flower_by_id(int(id))
        if flower != None:
            flowers.append(FlowerInfo(**flower.model_dump()))
            total_price += flower.price

    cart_json["flowers"] = flowers
    cart_json["total_price"] = total_price
    return cart_json


@app.post("/cart/items")
def add_to_cart(request: Request, response: Response, flower_id: int = Form(), user = Depends(get_current_user)):

    cart_raw = request.cookies.get("cart")
    if cart_raw == None:
        cart_raw = "[]"
    cart = json.loads(cart_raw)
    
    flower = flowerRep.get_flower_by_id(flower_id)

    if flower != None:
        cart.append(flower_id)
    
    response.set_cookie("cart", json.dumps(cart))
    return response

