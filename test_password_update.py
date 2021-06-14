from functions.base_functions import CrudUser
import time
import pytest


class TestPasswordUpdate:

    # Не додумал, как использовать username/password из фикстуры, тк проблема с зонами видимости.
    # А классовые переменные не меняются при итерациях. Решил через global не делать.
    # @pytest.fixture(scope="function", autouse=True)
    # def user_create(self):
    #     base = CrudUser()
    #     username = str(time.time())
    #     password = "password"
    #     base.send_registration_request(self.username, self.password, self.password)
    #     base.user_sign_in(self.username, self.password)

    password_positive = [
        "Strong_p@ssWord.123!",
        "weakpas",
        "weakpa",
        "ToomanycharsToomany",
        "ToomanycharsToomanyc"
    ]

    @pytest.mark.parametrize("new_pass", password_positive)
    def test_correct_password_update(self, new_pass):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, new_pass, new_pass)
        status = response.status_code
        json = response.json()
        assert status == 202, \
            f"Modified is not successful, expected status 202, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, new_pass)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    password_negative = [
        "weakp",
        "ToomanycharsToomanych",
        "",
        "      ",
        " pass ",
        "qwerty",
        "pass word",
        "сильныйпароль",
        "strongпароль",
        "123456"
    ]

    @pytest.mark.parametrize("new_pass", password_negative)
    def test_not_correct_password_update(self, new_pass):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, new_pass, new_pass)
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Password is '{new_pass}' Expected status 400, but got " \
            f"{status}. Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_not_correct_password_update_without_old_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, "", "newpassword", "newpassword")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_with_not_correct_old_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password + " ", "newpassword", "newpassword")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_with_not_equal_new_passwords(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, "newpassword1", "newpassword2")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_without_new_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, "", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_when_new_passwords_are_equal_with_old_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, password, password)
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_passwords_update_where_all_passwords_are_empty(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, "", "", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_without_username(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password("", password, password, password)
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_without_new_password_and_with_new_password_confirm(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, "", "newpassword2")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_password_update_with_new_password_and_without_password_confirm(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, password, "newpassword1", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_update_password_with_only_new_password_without_old_and_confirm(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, "", "newpassword1", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"

    def test_update_password_with_only_new_password_confirm_without_old_and_new_password(self):
        base = CrudUser()
        username = str(time.time())
        password = "password"
        base.send_registration_request(username, password, password)
        base.user_sign_in(username, password)

        response = base.update_password(username, "", "", "newpassword2")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Modified is successful, but not should be. Expected status 400, but got {status}. " \
            f"Json response is: {json}"

        final_response = base.user_sign_in(username, password)
        status = final_response.status_code
        json = final_response.json()
        assert status == 200, \
            f"Not correct authorization after password update. Expected status 200, but got {status}. " \
            f"Json response is: {json}"
