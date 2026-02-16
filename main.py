
from pathlib import Path
from faker import Faker

from src.core import Topic, User
from src.database import Database


fake = Faker()

def main():
	database = Database(Path("dataset.sql"))
	alice = User("Alice")
	bob = User("Bob")
	topic = Topic("topic")

	database.buffer_insert_user(bob)
	database.buffer_insert_user(alice)
	database.buffer_insert_topic(topic)

	database.user_pays_participation_fee(alice, 30)
	exchange = database.user_creates_exchange(alice, 3, topic)
	database.exchange_validates(exchange, bob, 3)
	
	database.flush_buffer()

if __name__ == "__main__":
	main()
