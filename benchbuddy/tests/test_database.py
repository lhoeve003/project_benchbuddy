import pytest
from db.database import init_db
# Controle of er op de juiste manier een databaseverbinding en cursor retourneert.
# Test of init_db() een geldige database connectie en cursor teruggeeft.
# Gemaakt met ChatGPT.


def test_init_db_returns_connection_and_cursor():
    conn, c = init_db()
    assert conn is not None
    assert c is not None
    conn.close()



