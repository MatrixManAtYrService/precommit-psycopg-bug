from sqlalchemy import URL, create_engine, NullPool
create_engine(
    URL.create(
        "postgresql+psycopg",
        host="127.0.0.1",
        username="foo",
        password="foo",
        database="foo",
    ), 
    isolation_level="AUTOCOMMIT", 
    poolclass=NullPool
) 


