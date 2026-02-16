
from __future__ import annotations

import json

from dataclasses import dataclass
from typing import Self

from mariadb import Connection
import mariadb


@dataclass
class Database:
    connection: Connection

    @classmethod
    def of_default_config(cls) -> Self:
        with open("database.json", "r", encoding="utf-8") as file:
            connection = mariadb.connect(**json.load(file))
            assert isinstance(connection, Connection)

        return cls(connection)

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def insert_user(self, name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"insert into User values (null, '{name}', null, null)")
