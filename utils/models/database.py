from __future__ import annotations

import string
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from utils.helpers import PREFIX_CONFIG_SCHEMA

import aiosqlite


class Record:
    __slots__ = ("arguments",)

    def __init__(self, arguments: Dict[str, Any]) -> None:
        self.arguments = arguments

    def __getitem__(self, __item: Union[str, int]) -> Any:
        if isinstance(__item, str):
            if __item in self.arguments:
                return self.arguments[__item]
            raise AttributeError(
                f'Dynamic object has no attribute \'{__item}\'')
        elif isinstance(__item, int):  # type: ignore
            return tuple(self.arguments.values())[__item]

    def __getattr__(self, __item: str):
        if __item in self.arguments:
            return self.arguments[__item]
        raise AttributeError(f"Dynamic object has no attribute '{__item}'")

    def __len__(self):
        return len(self.arguments.keys())

    def __repr__(self) -> str:
        argument = ", ".join(
            f"{key}={value}" for key, value in self.arguments.items()
        )
        return f"<Record: {argument}>"

    @classmethod
    def from_tuple(cls, arguments: Iterable[Any], tuple_: Iterable[Any]) -> Record:
        arguments = ["".join(map(lambda x: x if x in string.ascii_letters +
                             string.digits + '_' else "", arg)) for arg in arguments]
        return cls(dict(zip(arguments, tuple_)))

class Database:
    """
    Database class for storing opened connections

    Attributes
    ----------
    conn : Dict[str, aiosqlite.Connection]
        A dictionary of connections
    is_closed : bool
        Whether the connections are closed
    """

    def __init__(self):
        self.conn: Dict[str, aiosqlite.Connection] = {}
        self.is_closed: bool = False

    def __getattr__(self, __name: str) -> Any:
        if __name in self.conn:
            return self.conn[__name]
        return super().__getattribute__(__name)

    async def __aenter__(self) -> "Database":
        self.conn["config"] = await aiosqlite.connect("./databases/config.db")
        await self.init_dbs()
        return self

    async def init_dbs(self):
        async with self.cursor("config") as cursor:
            await cursor.execute(PREFIX_CONFIG_SCHEMA)

        await self.commit()

    async def __aexit__(self, *args: Any) -> None:
        await self.commit()
        await self.close()

    def cursor(self, conn: str) -> aiosqlite.Cursor:
        return getattr(self, conn).cursor()

    def __repr__(self) -> str:
        return f"<Database: {self.conn}>"

    async def select_record(
        self,
        connection: str,
        /,
        *,
        arguments: Tuple[str, ...],
        table: str,
        where: Optional[Tuple[str, ...]] = None,
        values: Optional[Tuple[Any, ...]] = None,
        extras: Optional[List[str]] = None,
    ) -> Optional[List[Record]]:
        statement = """SELECT {} FROM {}""".format(
            ", ".join(arguments), table
        )
        if where is not None:
            assign_question = map(lambda x: f"{x} = ?", where)
            statement += " WHERE {}".format(
                " AND ".join(assign_question)
            )
        if extras:
            for stuff in extras:
                statement += f" {stuff}"
        async with self.cursor(connection) as cursor:
            await cursor.execute(statement, values or ())
            # type: ignore # Type checker cries unnecessarily.
            rows: List[aiosqlite.Row[Any]] = [i async for i in cursor]
            if rows:
                return [Record.from_tuple(arguments, row) for row in rows]
            return None

    async def delete_record(
        self,
        connection: str,
        /,
        *,
        table: str,
        where: Tuple[str, ...],
        values: Optional[Tuple[Any, ...]] = None
    ) -> None:
        delete_statement = f"DELETE FROM {table}"
        if where is not None:
            assign_question = map(lambda x: f"{x} = ?", where)
            delete_statement += " WHERE {}".format(
                " AND ".join(assign_question))

        async with self.cursor(connection) as cursor:
            await cursor.execute(delete_statement, values or ())
            await getattr(self, connection).commit()

    async def insert_record(
        self,
        connection: str,
        /,
        *,
        table: str,
        values: Tuple[Any, ...],
        columns: Tuple[str, ...],
        extras: Optional[List[str]] = None
    ) -> None:

        insert_statement = """
                           INSERT INTO {}({}) VALUES ({})
                           """.format(
            table, ", ".join(columns), ", ".join(["?"] * len(columns))
        )
        if extras:
            for stuff in extras:
                insert_statement += f" {stuff}"
        async with self.cursor(connection) as cursor:
            await cursor.execute(insert_statement, values)
            await getattr(self, connection).commit()

    async def update_record(
        self,
        connection: str,
        /,
        *,
        table: str,
        to_update: Tuple[str, ...],
        where: Tuple[str, ...],
        values: Tuple[Any, ...],
        extras: Optional[List[str]] = None
    ) -> None:
        update_statement = """
                           UPDATE {} SET {} WHERE {}
                           """.format(
            table, ", ".join(
                map(lambda x: f"{x} = ?" if "=" not in x else x, to_update)),
            " AND ".join(map(lambda x: f"{x} = ?", where))
        )
        if extras:
            for stuff in extras:
                update_statement += f" {stuff}"
        async with self.cursor(connection) as cursor:
            await cursor.execute(update_statement, values)
            await getattr(self, connection).commit()

    @property
    def closed(self):
        return self.is_closed

    async def commit(self) -> None:
        for conn in self.conn.values():
            await conn.commit()

    async def close(self) -> None:
        self.is_closed = True
        for conn in self.conn.values():
            await conn.close()
