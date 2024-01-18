from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def privacy_policy(request):
    return render(request, 'account/privacy_policy.html')

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)
            return redirect('account_delete')
        else:
            messages.error(request, 'Invalid phone number or password.')

    return render(request, 'account/registration/login.html')

@login_required(login_url='login')
def delete_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Perform the account deletion logic here
            request.user.delete()
            logout(request)
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('login')  # Redirect to the delete success page

        return render(request, 'account/delete_account.html')
    else:
        return redirect('login')

