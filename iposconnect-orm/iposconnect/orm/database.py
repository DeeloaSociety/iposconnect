import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

load_dotenv()

POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "3"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "2"))
MAX_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))
POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"

POSTGRES_CONFIG = {
    "host": os.getenv("IPOS_POSTGRES_HOST"),
    "port": int(os.getenv("IPOS_POSTGRES_PORT")),
    "user": os.getenv("IPOS_POSTGRES_USER"),
    "password": os.getenv("IPOS_POSTGRES_PASSWORD"),
    "database": os.getenv("IPOS_POSTGRES_DATABASE"),
}


def database_url():
    """Return a database URL"""
    if not POSTGRES_CONFIG["host"]:
        raise Exception("IPOS_POSTGRES_HOST environment variable is required")
    if not POSTGRES_CONFIG["port"]:
        raise Exception("IPOS_POSTGRES_PORT environment variable is required")
    if not POSTGRES_CONFIG["user"]:
        raise Exception("IPOS_POSTGRES_USER environment variable is required")
    if not POSTGRES_CONFIG["password"]:
        raise Exception("IPOS_POSTGRES_PASSWORD environment variable is required")
    if not POSTGRES_CONFIG["database"]:
        raise Exception("IPOS_POSTGRES_DATABASE environment variable is required")
    return URL.create(
        drivername="postgresql+psycopg2",
        host=POSTGRES_CONFIG["host"],
        port=POSTGRES_CONFIG["port"],
        username=POSTGRES_CONFIG["user"],
        password=POSTGRES_CONFIG["password"],
        database=POSTGRES_CONFIG["database"],
    )


# Sync engine and session
engine = create_engine(
    database_url(),
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=MAX_TIMEOUT,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=POOL_PRE_PING,
    echo=False,
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Sync dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """Sync context manager for database sessions"""
    return get_db()


def get_connection_info():
    """Get current connection pool information for monitoring"""
    return {
        "pool_size": POOL_SIZE,
        "max_overflow": MAX_OVERFLOW,
        "pool_timeout": MAX_TIMEOUT,
        "pool_recycle": POOL_RECYCLE,
        "sync_engine": {
            "pool": engine.pool,
            "checked_out": engine.pool.checkedout(),
            "checked_in": engine.pool.checkedin(),
            "size": engine.pool.size(),
        },
    }
