#!/usr/bin/env python3
""" Integration tests module """
import requests


BASE_URL = "http://0.0.0.0:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ tests the register user endpoint """
    url = f"{BASE_URL}/users"
    data = {
        "email": email,
        "password": password
    }
    r = requests.post(url, data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}
    r = requests.post(url, data=data)
    assert r.status_code == 400
    assert r.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ tests the login endpoint with invalid cred """
    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }
    r = requests.post(url, data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ tests the logiv endpoint """
    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }
    r = requests.post(url, data=data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    assert r.cookies["session_id"] is not None
    assert type(r.cookies["session_id"]) is str
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    tests that unlogged user can't
    access profile endpoint
    """
    url = f"{BASE_URL}/profile"
    r = requests.get(url)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    tests profile endpoint with user logged in
    """
    url = f"{BASE_URL}/profile"
    cookies = dict(session_id=session_id)
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200


def log_out(session_id: str) -> None:
    """ logs a user out """
    url = f"{BASE_URL}/sessions"
    cookies = dict(session_id=session_id)
    r = requests.delete(url, cookies=cookies)
    assert r.status_code == 200
    r = requests.delete(url)
    assert r.status_code == 403


def reset_password_token(email: str) -> str:
    """ resets the password token """
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email
    }
    r = requests.post(url)
    assert r.status_code == 403
    r = requests.post(url, data=data)
    json_data = r.json()
    assert r.status_code == 200
    assert json_data.get("email") is not None
    assert json_data.get("reset_token") is not None
    return json_data.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ tests the update password routes """
    url = f"{BASE_URL}/reset_password"
    valid_data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    invalid_data = {
        "email": email,
        "reset_token": "invalid token",
        "new_password": new_password
    }
    r = requests.put(url, data=valid_data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}
    r = requests.put(url, invalid_data)
    assert r.status_code == 403


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
