from functions.base_functions import CrudUser
import time


class TestLoginUser:

    def test_that_user_can_sign_into_your_account(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        response = base.send_registration_request(username, password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in(username, password)
        status = response.status_code
        json = response.json()
        assert status == 200, \
            f"Trying to sign up with login '{username}' and password '{password}' is not correct. " \
            f"Expected status 200 but got {status}. Json response is: {json}"

    def test_that_user_cant_sign_into_your_account_without_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        response = base.send_registration_request(username, password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in(username, "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Trying to sign up with login '{username}' and without password successful, but should not be. " \
            f"Expected status 400 but got {status}. Json response is: {json}"

    def test_that_user_cant_sign_into_your_account_without_login(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        response = base.send_registration_request(username, password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in("", password)
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Trying to sign up without login and with password '{password}' successful, but should not be. " \
            f"Expected status 400 but got {status}. Json response is: {json}"

    def test_that_user_cant_sign_into_your_account_after_change_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        response = base.send_registration_request(username, password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in(username, password)
        status = response.status_code
        json = response.json()
        assert status == 200, \
            f"Trying to sign up with login '{username}' and password '{password}' is not correct. Expected status 200" \
            f" but got {status}. Json response is: {json}"

        response = base.update_password(username, password, "newpassword", "newpassword")
        status = response.status_code
        json = response.json()
        assert status == 202, \
            f"Modified is not successful, expected status 202, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in(username, password)
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Trying to sign up with login '{username}' and old password '{password}' after changing password to " \
            f"'newpassword' is successful, but not should be. Expected status 400 but got {status}. " \
            f"Json response is: {json}"

    def test_user_can_create_todos_after_sign_into_your_account_with_token(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        response = base.send_registration_request(username, password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in(username, password)
        status = response.status_code
        json = response.json()
        assert status == 200, \
            f"Trying to sign up with login '{username}' and password '{password}' is not correct. " \
            f"Expected status 200 but got {status}. Json response is: {json}"
        headers = {"Authorization": f"Bearer {json['access_token']}"}

        response = base.create_todo(username, headers, "smth")
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Trying to create todo list with login '{username}' and password '{password}' is not correct. " \
            f"Expected status 401 but got {status}. Json response is: {json}"

    def test_user_cant_create_todos_after_sign_into_your_account_without_token(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        response = base.send_registration_request(username, password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response = base.user_sign_in(username, password)
        status = response.status_code
        json = response.json()
        assert status == 200, \
            f"Trying to sign up with login '{username}' and password '{password}' is not correct. " \
            f"Expected status 200 but got {status}. Json response is: {json}"

        response = base.create_todo_without_token(username, "smth")
        status = response.status_code
        json = response.json()
        assert status == 401, \
            f"Trying to create todo list with login '{username}' and password '{password}' is not correct. " \
            f"Expected status 401 but got {status}. Json response is: {json}"
