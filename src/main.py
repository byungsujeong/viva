import uvicorn

from fastapi import FastAPI

from fastapi_pagination import add_pagination

from api import user, bulletinBoard


app = FastAPI()
app.include_router(user.router)
app.include_router(bulletinBoard.router)
add_pagination(app)


@app.get("/")
def health_check_handler():
    return {"health_check": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)