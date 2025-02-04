from fastapi import FastAPI
from app.routes.books import router as book_router
from app.routes.users import router as user_router
from app.routes.categories import router as category_router


app = FastAPI()

app.include_router(book_router)
app.include_router(user_router)
app.include_router(category_router)