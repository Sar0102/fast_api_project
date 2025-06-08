# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from starlette.testclient import TestClient
#
# from config import settings
# from infrastructure.database.base import Base
#
#
# engine = create_engine(settings.sync_database_url)
# TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# @pytest.fixture(scope="module", autouse=True)
# def setup_database():
#     """Set up the database for testing."""
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)
#
#
# @pytest.fixture(scope="function")
# def db_session():
#     """Create a new database session for a test."""
#     session = TestSessionLocal()
#     try:
#         yield session
#     finally:
#         session.rollback()
#         session.close()
#
#
# # @pytest.fixture(scope="module")
# # def client():
# #     """Create a test client for the application."""
# #
# #     def override_get_db():
# #         db = TestSessionLocal()
# #         try:
# #             yield db
# #         finally:
# #             db.close()
# #
# #     app.dependency_overrides[get_db] = override_get_db()
# #     client = TestClient(app)
# #     yield client
# #     app.dependency_overrides.clear()
