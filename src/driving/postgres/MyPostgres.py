# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager
from threading import Lock

import psycopg2
from psycopg2.pool import SimpleConnectionPool


class ConstantMyPostgres:
    POSTGRES_CONNECTION_ERROR = None


class MyPostgres:
    _connection_pool = None
    _lock = Lock()
    _ref_count = 0  # how many instances are using the pool

    def __init__(
        self,
        host="localhost",
        user="postgres",
        password="postgres",
        database="task",
        port=5432,
        minconn=1,
        maxconn=20,
    ):
        with MyPostgres._lock:
            if MyPostgres._connection_pool is None:
                try:
                    MyPostgres._connection_pool = SimpleConnectionPool(
                        minconn,
                        maxconn,
                        host=host,
                        user=user,
                        password=password,
                        database=database,
                        port=port,
                    )
                except psycopg2.DatabaseError as e:
                    print("Error while connecting to PostgreSQL:", e)
                    sys.exit(1)

            MyPostgres._ref_count += 1

    # -----------------------------
    # Context manager for cursors
    # -----------------------------
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
