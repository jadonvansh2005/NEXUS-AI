import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.session import SessionLocal
from models.user_fact import UserFact

db = SessionLocal()
try:
    facts = db.query(UserFact).all()
    count = 0
    for f in facts:
        val = f.fact_value.strip("?.!,- ")
        if not val or all(c in "?!.,- " for c in val):
            print(f"Deleting invalid fact: {f.fact_key} = {f.fact_value}")
            db.delete(f)
            count += 1
    db.commit()
    print(f"Successfully cleaned up {count} invalid facts from the database!")
finally:
    db.close()
