from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator

import psycopg
from flask import current_app
from psycopg.rows import dict_row


@contextmanager
def get_connection() -> Generator[psycopg.Connection, None, None]:
    database_url = current_app.config.get("DATABASE_URL")
    connect_kwargs = {
        "row_factory": dict_row,
    }

    if database_url:
        connect_kwargs["conninfo"] = database_url
    else:
        connect_kwargs.update(
            {
                "dbname": current_app.config["DB_NAME"],
                "user": current_app.config["DB_USER"],
                "password": current_app.config["DB_PASSWORD"],
                "host": current_app.config["DB_HOST"],
                "port": current_app.config["DB_PORT"],
            }
        )

    connection = psycopg.connect(**connect_kwargs)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def fetch_all(query: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return list(cursor.fetchall())


def fetch_one(query: str, params: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()


def execute(
    query: str,
    params: tuple[Any, ...] | None = None,
    *,
    fetchone: bool = False,
    fetchall: bool = False,
) -> Any:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return list(cursor.fetchall())
            return None
