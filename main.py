from fastapi import FastAPI

app = FastAPI()

@app.post("/token")
def token():
    return {
        "access_token": "teste_token",
        "type": "Bearer",
        "expires_in": "300",
        "refresh_token": "NaN"
    }

@app.get("/user/list")
def user_list():
    return {"key": "value"}