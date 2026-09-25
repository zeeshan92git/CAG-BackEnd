"""
In-memory data store for storing extracted PDF text.

This is a simple dict-based store. Data will be lost when the server restarts.
For production, migrate to a database (PostgreSQL, MongoDB, etc.)
"""

data_store = {}
