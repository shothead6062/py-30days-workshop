from demo_app.contracts import ValidationError, validate_user


def test_validate_user_ok():
    data = {"id": 1, "username": "alice", "email": "a@example.com", "role": "staff"}
    user = validate_user(data)
    assert user.id == 1
    assert user.username == "alice"
    assert user.email == "a@example.com"
    assert user.role == "staff"


def test_validate_user_fail_username_space():
    data = {"id": 2, "username": "a b", "email": "b@example.com"}
    try:
        validate_user(data)
    except ValidationError as e:
        # Should contain a message about spaces
        msgs = [err["msg"] for err in e.errors()]
        assert any("spaces" in m for m in msgs)
    else:
        raise AssertionError("Expected ValidationError for username with spaces")
