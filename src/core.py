
from __future__ import annotations

from bdb import effective
from dataclasses import dataclass, field
from enum import Enum


IDS: dict[str, int] = { }

def generate_id(name: str) -> int:
	global IDS
	id = IDS.get(name, 0)
	IDS[name] = id + 1
	return id

def generate_user_id() -> int:
	return generate_id("user")

def generate_exchange_id() -> int:
	return generate_id("exchange")

def generate_offer_id() -> int:
	return generate_id("offer")

def generate_participation_fee_id() -> int:
	return generate_id("participation fee")

def generate_skill_id() -> int:
	return generate_id("skill")

def generate_topic_id() -> int:
	return generate_id("topic")


class UserStatus(Enum):
	PAID = "PAID"
	UNPAID = "UNPAID"

@dataclass
class User:
	name: str
	id: int = field(default_factory=generate_user_id)
	status: UserStatus = UserStatus.UNPAID
	hours: int = 10

class ExchangeStatus(Enum):
	PLANNED = "PLANNED"
	DONE = "DONE"

@dataclass
class Exchange:
	source: User
	planned_hours: int
	id: int = field(default_factory=generate_exchange_id)
	effective_hours: int = 0
	status: ExchangeStatus = ExchangeStatus.PLANNED
	destination: User|None = None

@dataclass
class Offer:
	description: str
	hours: int
	skill: Skill
	id: int = field(default_factory=generate_offer_id)

@dataclass
class ParticipationFee:
	amount: int
	user: User
	id: int = field(default_factory=generate_participation_fee_id)

@dataclass
class Skill:
	name: str
	id: int = field(default_factory=generate_skill_id)

@dataclass
class Topic:
	name: str
	id: int = field(default_factory=generate_topic_id)
