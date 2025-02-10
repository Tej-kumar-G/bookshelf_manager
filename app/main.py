from fastapi import FastAPI
from app.routes.books import router as book_router
from app.routes.users import user_router
from app.routes.reviews import review_router
from app.routes.categories import category_router
from app.routes.authors import author_router

app = FastAPI()

app.include_router(book_router)
app.include_router(user_router)
app.include_router(review_router)
app.include_router(category_router)
app.include_router(author_router)