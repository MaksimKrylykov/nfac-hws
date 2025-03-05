from fastapi import FastAPI, Request
from math import factorial

app = FastAPI()

@app.get('/{num}')
def read_root(num):
    try:
        return {"nfactorial": factorial(int(num))}
    except:
        return {"nfactorial": "undefined"}
