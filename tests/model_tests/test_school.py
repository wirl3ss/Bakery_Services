import pytest
from sqlalchemy.exc import IntegrityError

from app.models.school import School

def test_create_school(session):
    school = School(
        name="ABcdef",
        adress="21 dowing street",
    )

    session.add(school)
    session.commit()

    assert school.id is not None
    assert school.name == "ABcdef"
    assert school.adress == "21 dowing street"
    assert school.created_at is not None

def test_query_school(session):
    school = School(
        name="ABcdef",
        adress="21 dowing street",
    )

    session.add(school)
    session.commit()

    school_id = school.id

    query = session.get(School, school_id)

    assert query.id is not None
    assert query.name == "ABcdef"
    assert query.adress == "21 dowing street"
    assert query.created_at is not None

def test_school_null_name(session):
    school = School(
        adress="21 dowing street",
    )

    with pytest.raises(IntegrityError):
        session.add(school)
        session.commit()

def test_school_null_adress(session):
    school = School(
        name="abcdef"
    )

    with pytest.raises(IntegrityError):
        session.add(school)
        session.commit()