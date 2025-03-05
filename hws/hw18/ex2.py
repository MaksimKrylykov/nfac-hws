from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/info')
def read_root(request: Request):
    return {"Method": request.method, "URL": request.url.path, "Port": request.url.port}
