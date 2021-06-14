from functions.base_functions import CrudUser
import pytest
import time


class TestUserCreatingPositive:

    username_positive = [
        "user1_na.me-tes't",                                            # заменить все на уникальные
        "Usernam",
        "userna",
        "UsernameUsernameUsernameUsernameUsernameUsernameU",
        "UsernameUsernameUsernameUsernameUsernameUsernameUs"
    ]

    @pytest.mark.parametrize("username", username_positive)
    def test_login_regular_registration_positive(self, username):
        base = CrudUser()
        response = base.send_registration_request(username, "password", "password")
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

    password_positive = [
        "Strong_p@ssWord.123!",
        "weakpas",
        "weakpa",
        "ToomanycharsToomany",
        "ToomanycharsToomanyc"
    ]

    @pytest.mark.parametrize("password", password_positive)
    def test_password_regular_registration_positive(self, password):
        base = CrudUser()
        response = base.send_registration_request(str(time.time()), password, password)
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with password '{password}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"


class TestUserCreatingNegative:

    username_negative = [
        "UsernameUsernameUsernameUsernameUsernameUsernameUse",
        "Usern",
        "qwerty",
        "",
        " user ",
        " userqwert",
        "userqwert ",
        "       ",
        "u sername",                                            # заменить на уникальный с пробелом
        "123456",
        "admin",
        "us@ername",
        "ТутМоглаБытьВашаSQLИньекция",
        "юзернейм",
        "[qwertyy",
        "q]wertyy",
        "qw{ertyy",
        "qwe~rtyy",
        "qwer<tyy",
        "qwert!yy",
        "qwerty*y",
        "qwertyy|",
        "qwer$tyy",
        "qwer%tyy",
        "qwer^tyy",
        "qwer&tyy",
        "qwer#tyy",
        "qwer/tyy",
        "qwer(tyy",
        "qwer)tyy",
        "qwer?tyy",
        "qwer}tyy",
        "qwer>tyy",
        "qwer,tyy",
        "<script>alert(123)</script>"
    ]

    @pytest.mark.parametrize("username", username_negative)
    def test_username_registration_negative(self, username):
        base = CrudUser()
        response = base.send_registration_request(username, "password", "password")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user with username '{username}' expected status is equal 400, but got {status}. " \
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
        "12"
    ]

    @pytest.mark.parametrize("password", password_negative)
    def test_password_registration_negative(self, password):
        base = CrudUser()
        response = base.send_registration_request(str(time.time()), password, password)
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user with password '{password}' expected status is equal 400, but got {status}. " \
            f"Json response is: {json}"

    def test_registration_with_password_without_confirm(self):
        base = CrudUser()
        response = base.send_registration_request(str(time.time()), "password", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user with password1 but without password2, expected status is equal 400, but got {status}. " \
            f"Json response is: {json}"

    def test_registration_without_password_with_confirm(self):
        base = CrudUser()
        response = base.send_registration_request(str(time.time()), "", "password")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user without password1 but with password2, expected status is equal 400, but got {status}. " \
            f"Json response is: {json}"

    def test_create_user_with_empty_fields(self):
        base = CrudUser()
        response = base.send_registration_request("", "", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user with empty fields, expected status is equal 400, but got {status}. " \
            f"Json response is: {json}"

    def test_create_user_with_only_password(self):
        base = CrudUser()
        response = base.send_registration_request("", "password", "")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user with only password1 and without password2, expected status is equal 400, but got {status}" \
            f". Json response is: {json}"

    def test_create_user_with_only_password_confirm(self):
        base = CrudUser()
        response = base.send_registration_request("", "", "password")
        status = response.status_code
        json = response.json()
        assert status == 400, \
            f"Creating user with only password2 and without password1, expected status is equal 400, but got {status}" \
            f". Json response is: {json}"

    exist_pass = [
        "password",
        "pass",
        ""
    ]

    @pytest.mark.parametrize("exist_password", exist_pass)
    def test_cant_create_user_with_data_already_existing_user(self, exist_password):
        base = CrudUser()
        username = str(time.time())
        response = base.send_registration_request(username, "password", "password")
        status = response.status_code
        json = response.json()
        assert status == 201, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status}. " \
            f"Json response is: {json}"

        response_check = base.send_registration_request(username, exist_password, exist_password)
        status_final = response_check.status_code
        json_final = response_check.json()
        assert status_final == 400, \
            f"Creating user with login '{username}' expected status is equal 201, but got {status_final}. " \
            f"Json response is: {json_final}"
