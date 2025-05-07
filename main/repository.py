from pathlib import Path
import json

from main.models import ContactsList

CONTACTS_FILE = Path(__file__).parent / "contacts.json"

class ContactsRepository:
    def __init__(self):
        self.file_path = CONTACTS_FILE

    def load_contacts(self) -> ContactsList:
        if not self.file_path.exists():
            raise FileNotFoundError("Contacts file not found.")
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            return ContactsList(**data)
        except json.JSONDecodeError:
            raise ValueError("Contacts file is not valid JSON.")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")