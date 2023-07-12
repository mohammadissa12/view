from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ninja import Router, File
from http import HTTPStatus
from ninja.files import UploadedFile
from django.contrib.auth import logout

from conf.utils.schemas import MessageOut
from conf.utils.permissions import AuthBearer, create_token
from conf.utils.utils import response
from .models import EmailAccount
from .schemas import AccountSignupOut, AccountSignupIn, AccountLoginIn, ChangePassword, AccountOut, AccountUpdateIn

auth_controller = Router(tags=['Auth'])


@auth_controller.post('/signup', response={200: AccountSignupOut, 403: MessageOut, 500: MessageOut})
def signup(request, payload: AccountSignupIn):
    if payload.password1 != payload.password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords does not match!'})
    try:
        EmailAccount.objects.get(phone_number=payload.phone_number)
        return response(403,
                        {'message': 'Forbidden, phone number is already registered'})
    except EmailAccount.DoesNotExist:
        pass

    try:
        EmailAccount.objects.get(email=payload.email)
        return response(403,
                        {'message': 'Forbidden, email is already registered'})

    except EmailAccount.DoesNotExist:
        user = EmailAccount.objects.create_user(first_name=payload.first_name, last_name=payload.last_name,
                                                email=payload.email, phone_number=payload.phone_number,
                                                password=payload.password1)
        if user:
            user.phone_number = payload.phone_number
            user.save()
            token = create_token(user.id)
            return response(200, {'profile': user, 'token': token})
        else:
            return response(500, {'message': 'Internal server error'})


@auth_controller.post('/login', response={200: AccountSignupOut, 404: MessageOut})
def login(request, payload: AccountLoginIn):
    try:
        user = EmailAccount.objects.get(phone_number=payload.phone_number)
        if user.check_password(payload.password):
            token = create_token(user.id)
            return response(200, {'profile': user, 'token': token})
    except EmailAccount.DoesNotExist:
        return response(404, {'message': 'User not found'})
    return response(404, {'message': 'User not found'})


@auth_controller.post('/change-password',
                      auth=AuthBearer(),
                      response={200: MessageOut, 400: MessageOut})
def change_password(request, payload: ChangePassword):
    if payload.new_password1 != payload.new_password2:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'Passwords do not match!'})

    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})

    user_update = authenticate(phone_number=user.phone_number, password=payload.old_password)

    if user_update is not None:
        user_update.set_password(payload.new_password1)
        user_update.save()
        return response(HTTPStatus.OK, {'message': 'password updated'})

    return response(HTTPStatus.BAD_REQUEST, {'message': 'something went wrong, please try again later'})


@auth_controller.get('/profile',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def profile(request):
    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})
    return response(HTTPStatus.OK, user)


@auth_controller.put('/profile',
                     auth=AuthBearer(),
                     response={200: AccountOut, 400: MessageOut})
def update_profile(request, user_in: AccountUpdateIn):
    try:
        user = get_object_or_404(EmailAccount, id=request.auth.id)
    except:
        return response(HTTPStatus.BAD_REQUEST, {'message': 'token missing'})

    if user_in.first_name:
        user.first_name = user_in.first_name
    if user_in.last_name:
        user.last_name = user_in.last_name
    if user_in.email:
        user.email = user_in.email
    if user_in.phone_number:
        user.phone_number = user_in.phone_number

    user.save()

    return response(HTTPStatus.OK, user)


from django.contrib.auth import logout


@auth_controller.post('/logout', auth=AuthBearer(), response={200: MessageOut, 400: MessageOut})
def user_logout(request):
    logout(request)
    request.session.flush()  # Delete the session data
    return response(HTTPStatus.OK, {'message': 'Logged out and session deleted successfully'})
