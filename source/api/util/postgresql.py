from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from api.util.helper import get_md5
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Text,
    Integer,
    DateTime,
    Boolean,
    insert,
    inspect,
    update,
)
from sqlalchemy.engine import Engine
from api.util.helper import get_md5, orm_to_dict , row_to_dict
# from sqlalchemy. import Engine


def get_db(engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session()
    try:
        yield db
    finally:
        db.close()


class PostgresqlService:
    _instance = {}

    def __new__(cls, *args, **kwargs):
        assert "url" in kwargs, "url is required to connect to Postgresql"

        key = get_md5(f'{kwargs["url"]}')
        if key not in cls._instance:
            cls._instance[key] = create_engine(
                kwargs["url"],
                pool_size=kwargs.get("pool_size", 5),
                max_overflow=kwargs.get("max_overflow", 10),
                pool_timeout=kwargs.get("pool_timeout", 30),  # biasanya 30 detik
                pool_recycle=kwargs.get("pool_recycle", 1800),  # 30 menit
                pool_pre_ping=True,
            )

        return cls._instance[key]


def auto_insert_table(table_name: str, schema_name: str, data: list, engine: Engine):
    metadata = MetaData(schema=schema_name if schema_name else None)

    inspector = inspect(engine)
    if not inspector.has_table(table_name, schema=schema_name):
        print(f"⚙️ Table '{schema_name}.{table_name}' belum ada, auto-create...")

        sample = data[0]
        columns = []

        for key, value in sample.items():

            if isinstance(value, bool):
                col_type = Boolean

            elif isinstance(value, int):
                col_type = Integer

            elif isinstance(value, datetime):
                col_type = DateTime

            else:
                if isinstance(value, str) and len(value) > 255:
                    col_type = Text
                else:
                    col_type = String

            columns.append(Column(key, col_type))

        table = Table(table_name, metadata, *columns, schema=schema_name)
        metadata.create_all(engine)

    else:
        metadata.reflect(bind=engine, schema=schema_name)
        table_key = f"{schema_name}.{table_name}" if schema_name else table_name
        table = metadata.tables[table_key]

    # Bulk insert
    with engine.connect() as conn:
        conn.execute(insert(table), data)
        conn.commit()


def auto_update_table(
    table_name: str, schema_name: str, data: list, engine: Engine, key_field: str = "id"
):
    metadata = MetaData(schema=schema_name)
    inspector = inspect(engine)

    if not inspector.has_table(table_name, schema=schema_name):
        raise ValueError(
            f"Tabel '{schema_name}.{table_name}' belum ada. Gunakan auto_insert_table dulu."
        )

    metadata.reflect(bind=engine, schema=schema_name)
    table = metadata.tables[f"{schema_name}.{table_name}"]

    with engine.connect() as conn:
        for record in data:
            if key_field not in record:
                raise ValueError(
                    f"Data tidak punya key field '{key_field}' untuk update: {record}"
                )

            stmt = (
                update(table)
                .where(table.c[key_field] == record[key_field])
                .values({k: v for k, v in record.items() if k != key_field})
            )
            result = conn.execute(stmt)

            if result.rowcount == 0:
                conn.execute(insert(table).values(record))

        conn.commit()

def get_one(table_name: str, schema_name: str, db: Session, key_field: str, value: str):
    metadata = MetaData(schema=schema_name)

    table = Table(
        table_name,
        metadata,
        autoload_with=db.bind,
        schema=schema_name
    )

    column = table.c.get(key_field)
    if column is None:
        raise Exception(f"Column {key_field} not found in {table_name}")

    result = db.query(table).filter(column == value).first()
    print(result)

    return row_to_dict(result) if result else None