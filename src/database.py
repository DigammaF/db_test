
from __future__ import annotations

import json

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterator, Self

from .core import Exchange, ExchangeStatus, Offer, ParticipationFee, Skill, Topic, User


@dataclass
class Database:
	path: Path
	buffer: list[str] = field(default_factory=list[str])
	users: list[User] = field(default_factory=list[User])
	exchanges: list[Exchange] = field(default_factory=list[Exchange])

	def __post_init__(self):
		with open(self.path, "w", encoding="utf-8") as file:
			file.write("")

	def fmt_value(self, value: Any) -> str:
		if value is None:
			return "NULL"

		if isinstance(value, str):
			return f"'{value}'"
		
		return str(value)

	def flush_buffer(self):
		self.write(iter(self.buffer))
		self.buffer.clear()

	def write(self, lines: Iterator[str]):
		with open(self.path, "a", encoding="utf-8") as file:
			for line in lines:
				file.write(line + "\n")

	def make_insert(self, table: str, map: dict[str, Any]) -> str:
		columns = tuple(map)
		values = tuple(
			self.fmt_value(map[column]) for column in columns
		)
		return f"insert into {table}({','.join(columns)}) values({','.join(values)})"

	def buffer_insert(self, table: str, map: dict[str, Any]):
		self.buffer.append(self.make_insert(table, map))

	def make_update(self, table: str, id: int, map: dict[str, Any]) -> str:
		values = ",".join(f"{key}={self.fmt_value(value)}" for key, value in map.items())
		return f"update {table} set {values} where id={id}"
	
	def buffer_update(self, table: str, id: int, map: dict[str, Any]):
		self.buffer.append(self.make_update(table, id, map))

	def buffer_insert_exchange(self, exchange: Exchange):
		self.exchanges.append(exchange)
		self.buffer_insert(
			"Exchange", {
				**asdict(exchange), "status": exchange.status.value,
				"source": exchange.source.id
			}
		)

	def buffer_insert_offer(self, offer: Offer):
		self.buffer_insert(
			"Offer", {
				**asdict(offer), "skill": offer.skill.id
			}
		)

	def buffer_insert_participation_fee(self, participation_fee: ParticipationFee):
		self.buffer_insert(
			"ParticipationFee", {
				**asdict(participation_fee),
				"user": participation_fee.user.id,
			}
		)

	def buffer_insert_skill(self, skill: Skill):
		self.buffer_insert(
			"Skill", {
				**asdict(skill)
			}
		)

	def buffer_insert_topic(self, topic: Topic):
		self.buffer_insert(
			"Topic", {
				**asdict(topic)
			}
		)

	def buffer_insert_user(self, user: User):
		self.users.append(user)
		self.buffer_insert(
			"User", {
				**asdict(user), "status": user.status.value
			}
		)

	def buffer_insert_skill_user_relation(self, skill: Skill, user: User):
		self.buffer.append(f"insert into SkillUserRelation(skill, user) values({skill.id}, {user.id})")

	def buffer_insert_topic_exchange_relation(self, topic: Topic, exchange: Exchange):
		self.buffer.append(f"insert into TopicExchangeRelation(topic, exchange) values({topic.id}, {exchange.id})")

	def buffer_insert_skill_topic_relation(self, skill: Skill, topic: Topic):
		self.buffer.append(f"insert into SkillTopicRelation(skill, topic) values({skill.id}, {topic.id})")

	# -------------------------------------------------------------------------

	def user_pays_participation_fee(self, user: User, amount: int):
		self.buffer_insert_participation_fee(ParticipationFee(amount, user))

	def user_creates_exchange(self, user: User, planned_hours: int, topic: Topic) -> Exchange:
		exchange = Exchange(user, planned_hours)
		self.buffer_insert_exchange(exchange)
		self.buffer_insert_topic_exchange_relation(topic, exchange)
		return exchange

	def exchange_validates(self, exchange: Exchange, destination: User, effective_hours: int):
		exchange.effective_hours = effective_hours
		exchange.status = ExchangeStatus.DONE
		exchange.destination = destination
		self.buffer_update(
			"Exchange", exchange.id, {
				"effective_hours": effective_hours,
				"status": ExchangeStatus.DONE.value,
				"destination": destination.id
			}
		)
