from pathlib import Path
from json import JSONDecodeError, load, dump
from typing import List
from main.models import Contact, ContactsList

CONTACTS_FILE = Path(__file__).parent / "contacts.json"

class ContactsRepository:
    def __init__(self):
        self.file_path = CONTACTS_FILE

    # load contacts from JSON file
    def load_contacts(self) -> ContactsList:
        if not self.file_path.exists():
            raise FileNotFoundError("Contacts file not found.")
        try:
            with open(self.file_path, "r") as f:
                data = load(f)
            return ContactsList(**data)
        except JSONDecodeError:
            raise ValueError("Contacts file is not valid JSON.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")

    # save contacts to JSON file
    def save_contacts(self, contacts: List[Contact]):
        for contact in contacts:
            if not isinstance(contact, Contact):
                raise ValueError("Invalid contact in list")
            tmp_path = self.file_path.with_suffix(".tmp")
            with open(tmp_path, "w") as f:
                dump({"contacts": [contact.dict() for contact in contacts]}, f, indent=2)
            tmp_path.replace(self.file_path)