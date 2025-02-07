# app/main.py
from fastapi import FastAPI
from app.routes.books import router as book_router
from app.routes.authors import router as author_router
from app.routes.users import router as user_router
from app.routes.reviews import router as review_router
from app.routes.categories import router as category_router 
from app.routes.publishers import router as publisher_router
from app.routes.bookstores import router as bookstore_router
from app.routes.search import router as search_router

app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)
app.include_router(user_router)
app.include_router(review_router)
app.include_router(category_router)
app.include_router(publisher_router)
app.include_router(bookstore_router)
app.include_router(search_router)
