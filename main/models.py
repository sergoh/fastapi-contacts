from typing import List

from pydantic import BaseModel


class Contact(BaseModel):
    first_name: str
    last_name: str
    zip_code: str
    phone_number: str
    last_contacted: str

class ContactsList(BaseModel):
    contacts: List[Contact]