# db.py
import os
from supabase import create_client, Client

# load these from your env or .env file
SUPABASE_URL = "https://yhumjtjhxjujznfquqlj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlodW1qdGpoeGp1anpuZnF1cWxqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUxOTQ4NDcsImV4cCI6MjA2MDc3MDg0N30.ue-b2n2ebu1VH7yRnMo4Qegs-A29YW3aNkT3rGYNulU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def read_attendees():
    """
    Returns a list of dicts: [{"name":..., "Q1":..., "Q2":...}, …]
    """
    Responses = (
        supabase
        .table("Responses")
        .select("name, Q1, Q2")
        .execute()
    )
    return Responses.data  # each item is a Python dict

def append_attendee(name: str, Q1: str, Q2: str):
    """
    Inserts one row into Responses.
    """
    supabase.table("Responses").insert({
        "name": name,
        "Q1": Q1,
        "Q2": Q2
    }).execute()
