
from faker import Faker

from src.database import Database


fake = Faker()

def main():
    with Database.of_default_config() as database:
        for _ in range(3):
            database.insert_user(fake.name())

if __name__ == "__main__":
    main()
