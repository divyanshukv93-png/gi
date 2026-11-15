"""Create an admin account: python -m app.create_admin you@example.com"""
import getpass, sys
from app.core.security import hash_password
from app.database.session import Base, SessionLocal, engine
from app.models.models import User

Base.metadata.create_all(engine)
email, pw = sys.argv[1].lower(), getpass.getpass("Password (min 8 chars): ")
if len(pw) < 8: sys.exit("Password too short")
with SessionLocal() as db:
    db.add(User(email=email, hashed_password=hash_password(pw), role="admin")); db.commit()
print("Admin created")
