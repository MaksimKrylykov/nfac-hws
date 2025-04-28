from fastapi import FastAPI, Request

app = FastAPI()

@app.post('/meaning-of-life')
def read_root(request: Request):
    return {"meaning": "42"}
