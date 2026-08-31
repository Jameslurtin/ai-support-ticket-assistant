from fastapi import FastAPI
from pydantic import BaseModel

from database import create_table, insert_ticket, get_all_tickets
from ai_service import analyze_ticket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()


class Ticket(BaseModel):
    title: str
    description: str


@app.get("/")
def home():
    return {
        "message": "AI Support Assistant API is running"
    }


@app.post("/tickets")
def create_ticket(ticket: Ticket):

    analysis = analyze_ticket(
        ticket.title,
        ticket.description
    )

    status = "created"

    ticket_id = insert_ticket(
        ticket.title,
        ticket.description,
        status,
        analysis["category"],
        analysis["priority"],
        analysis["summary"],
        analysis["suggested_action"]
    )

    return {
        "id": ticket_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": status,
        "category": analysis["category"],
        "priority": analysis["priority"],
        "summary": analysis["summary"],
        "suggested_action": analysis["suggested_action"]
    }


@app.get("/tickets")
def list_tickets():

    rows = get_all_tickets()

    tickets = []

    for row in rows:
        tickets.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "category": row[4],
            "priority": row[5],
            "summary": row[6],
            "suggested_action": row[7]
        })

    return tickets