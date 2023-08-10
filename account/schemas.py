from ninja import Schema
from pydantic import EmailStr, UUID4, HttpUrl

from conf.utils.schemas import Token


class AccountOut(Schema):
    id: UUID4
    email: EmailStr = None
    first_name: str
    last_name: str
    phone_number: int
    image_url: HttpUrl = None


class AccountSignupIn(Schema):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    phone_number: int
    password1: str
    password2: str


class AccountSignupOut(Schema):
    profile: AccountOut
    token: Token


class AccountLoginIn(Schema):
    phone_number: int
    password: str


class AccountUpdateIn(Schema):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    phone_number: int


class ImageUpdateIn(Schema):
    image: str = None


class ChangePassword(Schema):
    old_password: str
    new_password1: str
    new_password2: str


class Profile(Schema):
    id: UUID4
    account: AccountOut


class AppDetails(Schema):
    app_version: str = None


class MerchantOut(Schema):
    id: UUID4
    account: AccountOut