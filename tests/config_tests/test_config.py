from app.core.config import settings

def test_settings():
    assert settings.PROJECT_NAME == "Bakery Services"
    assert settings.DEBUG is False
    assert settings.DATABASE_URL == "postgresql+psycopg2://postgres_user:postgres_password@localhost/my_database"
    assert settings.SECRET_KEY == "n"
    assert settings.ALGORITHM == "n"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30