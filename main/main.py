from fastapi import FastAPI, HTTPException

from main.models import ContactsList
from main.repository import ContactsRepository

app = FastAPI()

contacts_repo = ContactsRepository()

@app.get("/contacts", response_model=ContactsList)
def get_contacts():
    try:
        contacts = contacts_repo.load_contacts()
        return contacts
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Contacts file not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")