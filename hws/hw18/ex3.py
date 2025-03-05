from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/')
def read_root(request: Request):
    return {"message": "Hello, nfactorial!"}
