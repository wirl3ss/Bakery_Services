import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models.user import User
from app.models.student import Student
from app.models.shop import Shop
from app.models.calendar_exception import CalendarException
from app.models.order import Order
from app.models.product import Product
from app.models.school import School
from app.models.weekly_schedule import WeeklySchedule

@pytest.fixture
def session():
    engine = create_engine("sqlite://")

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()