import pytest
from app.users.dao import UsersDAO

@pytest.mark.parametrize("user_id, exists, email",  [
    (1, True, "test@test.com"),
    (2, True, "vlad@example.com"),
    (3, False, "..."),
])
async def test_find_user_by_id(user_id, exists, email):
    user = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user
