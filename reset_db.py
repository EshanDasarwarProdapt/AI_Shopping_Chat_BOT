from database import engine, Base
import seed_data
from models import Product, User, ChatSession

def reset():
    print("Dropping tables...")
    Base.metadata.drop_all(bind=engine)
    print("Recreating tables and seeding...")
    seed_data.seed()
    
if __name__ == "__main__":
    reset()
