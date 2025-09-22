from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path

# SQLAlchemy imports
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI(title="Books R Us API", version="1.0.0")

# Data models
class BookBase(BaseModel):
    book_name: str
    author: str
    publisher: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    book_name: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None

class Book(BookBase):
    id: int


# -----------------------------
# Database setup (SQLAlchemy)
# -----------------------------
# Use books.db from previous assignment, located at the repository root.
# Create separate table for API
DB_PATH = (Path(__file__).resolve().parent.parent / "books.db")
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class BookORM(Base):
    __tablename__ = "books_api"

    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)


Base.metadata.create_all(engine)


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return {"message": "Welcome to Books R Us"}


@app.post("/books", response_model=Book, status_code=201)
def create_book(payload: BookCreate, session: Session = Depends(get_session)):
    row = BookORM(**payload.model_dump())
    session.add(row)
    session.commit()
    session.refresh(row)
    return Book(id=row.id, book_name=row.book_name, author=row.author, publisher=row.publisher)


@app.get("/books", response_model=List[Book])
def list_books(session: Session = Depends(get_session)):
    rows = session.execute(select(BookORM).order_by(BookORM.id)).scalars().all()
    return [Book(id=r.id, book_name=r.book_name, author=r.author, publisher=r.publisher) for r in rows]


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    row = session.get(BookORM, book_id)
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(id=row.id, book_name=row.book_name, author=row.author, publisher=row.publisher)


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookCreate, session: Session = Depends(get_session)):
    row = session.get(BookORM, book_id)
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    data = payload.model_dump()
    row.book_name = data["book_name"]
    row.author = data["author"]
    row.publisher = data["publisher"]
    session.commit()
    session.refresh(row)
    return Book(id=row.id, book_name=row.book_name, author=row.author, publisher=row.publisher)


@app.patch("/books/{book_id}", response_model=Book)
def patch_book(book_id: int, payload: BookUpdate, session: Session = Depends(get_session)):
    row = session.get(BookORM, book_id)
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")

    patch = payload.model_dump(exclude_unset=True)
    if patch.get("book_name") is not None:
        row.book_name = patch["book_name"]
    if patch.get("author") is not None:
        row.author = patch["author"]
    if patch.get("publisher") is not None:
        row.publisher = patch["publisher"]
    session.commit()
    session.refresh(row)
    return Book(id=row.id, book_name=row.book_name, author=row.author, publisher=row.publisher)


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    row = session.get(BookORM, book_id)
    if not row:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(row)
    session.commit()
    return None


# DEV mode
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
