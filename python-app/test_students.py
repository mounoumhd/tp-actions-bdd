
import pytest
import psycopg2

from students import add_student, get_student, average_grade


@pytest.fixture
def conn():
    connection = psycopg2.connect(
        host="localhost",
        database="tp",
        user="postgres",
        password="postgres"
    )

    with connection.cursor() as cur:
        cur.execute("TRUNCATE TABLE students RESTART IDENTITY")
    connection.commit()

    yield connection

    connection.close()


def test_ajouter_et_lire(conn):
    add_student(conn, "Mounia", 15)
    
    student = get_student(conn, 1)

    assert student[1] == "Mounia"
    assert float(student[2]) == 15.0


def test_etudiant_inexistant(conn):
    student = get_student(conn, 999)

    assert student is None


def test_moyenne(conn):
    add_student(conn, "Amel", 10)
    add_student(conn, "Karim", 14)

    assert average_grade(conn) == 12.0
