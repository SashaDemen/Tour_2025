# +


from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()


# об`єкт класу, де прописуємо шлях до теки, бо програма не розуміє
templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory="static"), name="static")


app.add_middleware(SessionMiddleware, secret_key="your-secret-key")