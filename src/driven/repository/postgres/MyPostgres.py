# -*- coding: utf-8 -*-
import logging
import sys
from contextlib import contextmanager
from threading import Lock
from typing import NamedTuple

import psycopg2
from psycopg2.pool import SimpleConnectionPool


class PostgresConfig(NamedTuple):
    host: str
    user: str
    password: str
    database: str
    port: int
    minconn: int
    maxconn: int


class MyPostgres:
    driving_component = "REPOSITORY_POSTGRES"
    _connection_pool = None
    _lock = Lock()
    _ref_count = 0

    def __init__(
        self,
        config: PostgresConfig,
        console_log: logging.Logger,
        event_log: logging.Logger,
    ):
        self.console_log = console_log
        self.event_log = event_log

        with MyPostgres._lock:
            if MyPostgres._connection_pool is None:
                try:
                    MyPostgres._connection_pool = SimpleConnectionPool(
                        config.minconn,
                        config.maxconn,
                        host=config.host,
                        user=config.user,
                        password=config.password,
                        database=config.database,
                        port=config.port,
                    )
                except psycopg2.DatabaseError as e:
                    print("Error while connecting to PostgreSQL:", e)
                    sys.exit(1)

            MyPostgres._ref_count += 1

    @contextmanager
    def get_cursor(self):
        connection = None
        cursor = None
        try:
            connection = MyPostgres._connection_pool.getconn()
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception:
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                MyPostgres._connection_pool.putconn(connection)

    # -----------------------------
    # Query helpers
    # -----------------------------
    def execute_query(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)

    def fetch_all(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    # -----------------------------
    # Pool lifecycle management
    # -----------------------------
    def close(self):
        with MyPostgres._lock:
            MyPostgres._ref_count -= 1
            if MyPostgres._ref_count == 0 and MyPostgres._connection_pool:
                MyPostgres._connection_pool.closeall()
                MyPostgres._connection_pool = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
