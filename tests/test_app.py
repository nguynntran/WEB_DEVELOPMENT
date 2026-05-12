from app.models import User


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200


def test_register_creates_user(client, app):
    response = client.post(
        "/register",
        data={
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "test_password",
        },
        follow_redirects=False,
    )

    assert response.status_code in (302, 303)

    with app.app_context():
        created_user = User.query.filter_by(username="test_user").first()
        assert created_user is not None
