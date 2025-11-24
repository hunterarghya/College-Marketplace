from app.database import engine, Base
from app import model 

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("Recreating all tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
