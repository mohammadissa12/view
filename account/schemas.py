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
    is_merchant: bool
    is_free: bool
    days_to_expire: str = None


class AccountSignupIn(Schema):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    phone_number: int
    password1: str
    password2: str


class SignInOut(Schema):
    id: UUID4
    first_name: str
    last_name: str
    phone_number: int
    image_url: HttpUrl = None
    is_merchant: bool
    is_free: bool
    days_to_expire: str = None



class AccountSignupOut(Schema):
    profile: AccountOut
    token: Token


class AccountSignInOut(Schema):
    profile: SignInOut
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


class AppDetails(Schema):
    app_version: str = None
    android_link: str = None
    ios_link: str = None

