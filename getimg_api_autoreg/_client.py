from typing import Optional, Dict, Any

import re
import time

import httpx
from disposablemail import DisposableMail

from ._utils import generate_string


class MailClient(DisposableMail):
    def __init__(self) -> None:
        super().__init__()

    def get_verify_url(self) -> str:
        new_message = self.wait_message()
        message_id = new_message.id

        message_content = self.get_message(message_id)

        verify_url = self._extract_verify_url(message_content)
        return verify_url

    def _extract_verify_url(self, html_content: str) -> str:
        match = re.search(r'href="(https:\/\/u2293344[^"]+)', html_content, re.M)
        if not match:
            raise NotImplementedError("Could not extract verification url")
        return match.group(1)


class AuthClient:
    _client: httpx.Client

    username: str
    password: str

    base_url = "https://api.getimg.ai/dashboard"

    def __init__(self) -> None:
        self._client = httpx.Client(base_url=self.base_url)
        self._generate_user_data()

    def __enter__(self) -> "AuthGetImg":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def sign_up(self, email: str) -> Dict[str, Any]:
        payload = {
            "email": email,
            "username": self.username,
            "password": self.password,
            "confirmPassword": self.password,
        }
        response = self._client.post("/me", json=payload)
        return response.json()

    def sign_in(self, email: str) -> Dict[str, Any]:
        payload = {"email": email, "password": self.password}
        response = self._client.post("/auth", json=payload)
        return response.json()

    def create_api_key(self) -> Dict[str, Any]:
        payload = {"name": generate_string()}
        response = self._client.post("/keys", json=payload)
        return response.json()

    def _generate_user_data(self) -> None:
        self.username = generate_string()
        self.password = generate_string()


class GetimgAutoreg:
    _auth_client: AuthClient
    _mail_client: MailClient

    email: str

    def __init__(
        self,
        *,
        auth_client: Optional[AuthClient] = None,
        mail_client: Optional[MailClient] = None,
    ) -> None:
        self._auth_client = auth_client or AuthClient()
        self._mail_client = mail_client or MailClient()

    def __enter__(self) -> "GetimgAutoreg":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def close(self) -> None:
        if hasattr(self, "_auth_client"):
            self._auth_client.close()
        if hasattr(self, "_mail_client"):
            self._mail_client.close()

    def register_account(self) -> None:
        email_data = self._mail_client.get_email()
        self.email = email_data.email

        register_data = self._auth_client.sign_up(self.email)
        if not register_data.get("success"):
            raise NotImplementedError("Failed to register account")

    def activate_account(self) -> None:
        verify_url = self._mail_client.get_verify_url()

        response = self._auth_client._client.get(verify_url)
        if response.status_code != 302:
            raise NotImplementedError("Failed to activate account")

    def get_api_key(self) -> str:
        self._auth_client.sign_in(self.email)

        api_key_data = self._auth_client.create_api_key()
        if api_key := api_key_data.get("key"):
            return api_key
        raise NotImplementedError("Failed to get API key")
