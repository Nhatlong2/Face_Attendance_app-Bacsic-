import pytest
from services.db_service import DatabaseService
from services.user_service import UserService

def test_add_and_list_user():
    db = DatabaseService()
    users = UserService(db)
    users.add_user_returning_id("TestUser")
    result = users.list_users()
    assert any(u[1] == "TestUser" for u in result)
    db.close()
