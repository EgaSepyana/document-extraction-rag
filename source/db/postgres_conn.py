from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from api.util.helper import get_md5
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    insert,
    inspect,
    update,
)
from sqlalchemy.engine import Engine


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
    metadata = MetaData(schema=None)

    if schema_name:
        metadata = MetaData(schema=schema_name)

    # 3. Cek apakah tabel sudah ada
    inspector = inspect(engine)
    if not inspector.has_table(table_name, schema=schema_name):
        print(f"⚙️ Table '{schema_name}.{table_name}' belum ada, auto-create...")

        sample = data[0]
        columns = []
        for key, value in sample.items():
            if isinstance(value, int):
                col_type = Integer
            else:
                col_type = String
            columns.append(Column(key, col_type))

        table = Table(table_name, metadata, *columns, schema=schema_name)
        metadata.create_all(engine)
    else:
        metadata.reflect(bind=engine, schema=schema_name)
        table = metadata.tables[f"{schema_name}.{table_name}"]

    # 4. Bulk insert
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
