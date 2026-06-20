from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import engine, get_db, Base
from app import models, schemas

# Creates all tables defined in models.py, if they don't already exist.
# Later we'll switch to Alembic migrations for changes, but this is fine to start.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")


@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}


@app.post("/transactions", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    if not transaction.items:
        raise HTTPException(status_code=400, detail="A transaction needs at least one item")

    db_transaction = models.Transaction(
        date=transaction.date,
        description=transaction.description,
        account=transaction.account,
    )

    for item in transaction.items:
        db_transaction.items.append(
            models.TransactionItem(
                category_id=item.category_id,
                amount=item.amount,
                notes=item.notes,
            )
        )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions", response_model=List[schemas.TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    transactions = (
        db.query(models.Transaction)
        .options(joinedload(models.Transaction.items))
        .order_by(models.Transaction.date.desc())
        .all()
    )
    return transactions


@app.post("/categories", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories", response_model=List[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()