from sqlalchemy import text
from db import get_db

with get_db() as db:
    result = db.execute(text("SELECT 1"))
    print("Database connection successful:", result.scalar())