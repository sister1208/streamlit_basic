from urllib.parse import quote_plus

import streamlit as st
from sqlalchemy import create_engine, text


@st.cache_resource
def get_engine():
    """MySQL 연결 풀을 생성하고 애플리케이션 전체에서 재사용"""
    db = st.secrets["mysql"]
    password = quote_plus(str(db["password"]))
    url = (
        f"mysql+pymysql://{db['user']}:{password}"
        f"@{db['host']}:{db['port']}/{db['database']}"
        f"?charset={db.get('charset', 'utf8mb4')}"
    )
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
    )


def test_connection():
    with get_engine().connect() as connection:
        return connection.execute(text("SELECT 1")).scalar_one()
