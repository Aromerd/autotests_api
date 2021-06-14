from functions.locators import Locators
import requests


class CrudUser:

    @staticmethod
    def update_password(username, old, pass1, pass2):
        response = requests.put(
            Locators.CREATE_AND_UPDATE_USER_LINK,
            json={"username": username, "old_password": old, "password1": pass1, "password2": pass2}
        )
        return response

    @staticmethod
    def send_registration_request(username, pass1, pass2):
        response = requests.post(
            Locators.CREATE_AND_UPDATE_USER_LINK,
            json={"username": username, "password1": pass1, "password2": pass2}
        )
        return response

    @staticmethod
    def user_sign_in(username, password):
        response = requests.post(
            Locators.SIGN_IN_USER_LINK,
            json={"username": username, "password": password}
        )
        return response

    @staticmethod
    def create_todo(username, headers, text):
        response = requests.post(
            Locators.TODOS_LINK + username,
            headers=headers,
            json={"text": text, "status": "TODO"}
        )
        return response

    @staticmethod
    def create_todo_without_token(username, text):
        response = requests.post(
            Locators.TODOS_LINK + username,
            json={"text": text, "status": "TODO"}
        )
        return response
