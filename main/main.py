from fastapi import FastAPI, HTTPException, Body

from main.models import ContactsList, Contact
from main.repository import ContactsRepository

app = FastAPI()

contacts_repo = ContactsRepository()

# get all contacts
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

# partial update a contact attribute
@app.put("/update_contacts/{contact_id}")
def update_contact(contact_id: int, data):
    contacts = contacts_repo.load_contacts().contacts
    found = False
    for contact in contacts:
        if contact.id == contact_id:
            found = True
            if "first_name" in data:
                contact.first_name = data["first_name"]
            if "last_name" in data:
                contact.last_name = data["last_name"]
            if "zip_code" in data:
                contact.zip_code = data["zip_code"]
            if "phone_number" in data:
                contact.phone_number = data["phone_number"]
            if "last_contacted" in data:
                contact.last_contacted = data["last_contacted"]
            contacts_repo.save_contacts(contacts)
            return {"message": "Contact updated"}, 201  
    if not found:
        return {"error": "Contact not found"}, 400  