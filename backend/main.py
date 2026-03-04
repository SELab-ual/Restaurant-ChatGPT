import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="RMOS Sprint 1 Prototype")

# ---------------- Models ----------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    role = Column(String)

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="inactive")
    waiter_id = Column(Integer, ForeignKey("users.id"))
    waiter = relationship("User")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    status = Column(String, default="pending")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    name = Column(String)
    status = Column(String, default="pending")

Base.metadata.create_all(bind=engine)

# ---------------- Schemas ----------------
class LoginRequest(BaseModel):
    username: str
    role: str

class ActivateTableRequest(BaseModel):
    waiter_id: int

class CreateOrderRequest(BaseModel):
    table_id: int
    items: list[str]

# ---------------- Sample menu ----------------
MENU = [
    {"name": "Pizza"},
    {"name": "Burger"},
    {"name": "Salad"},
]

# ---------------- Endpoints ----------------
@app.get("/menu")
def get_menu():
    return MENU

@app.post("/login")
def login(req: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter_by(username=req.username).first()
    if not user:
        user = User(username=req.username, role=req.role)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"user_id": user.id, "role": user.role}

@app.post("/tables/{table_id}/activate")
def activate_table(table_id: int, req: ActivateTableRequest):
    db = SessionLocal()
    table = db.query(Table).filter_by(id=table_id).first()
    if not table:
        table = Table(id=table_id, waiter_id=req.waiter_id, status="active")
        db.add(table)
    else:
        table.status = "active"
        table.waiter_id = req.waiter_id
    db.commit()
    return {"status": "active"}

@app.post("/orders")
def create_order(req: CreateOrderRequest):
    db = SessionLocal()
    order = Order(table_id=req.table_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in req.items:
        db.add(OrderItem(order_id=order.id, name=item))
    db.commit()
    return {"order_id": order.id}

@app.post("/orders/{order_id}/accept")
def accept_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(404)
    order.status = "accepted"
    db.commit()
    return {"status": "accepted"}

@app.post("/items/{item_id}/ready")
def mark_ready(item_id: int):
    db = SessionLocal()
    item = db.query(OrderItem).get(item_id)
    if not item:
        raise HTTPException(404)
    item.status = "ready"
    db.commit()
    return {"status": "ready"}

@app.post("/items/{item_id}/deliver")
def mark_delivered(item_id: int):
    db = SessionLocal()
    item = db.query(OrderItem).get(item_id)
    if not item:
        raise HTTPException(404)
    item.status = "delivered"
    db.commit()
    return {"status": "delivered"}

@app.get("/orders")
def list_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    return [{"id": o.id, "status": o.status} for o in orders]
