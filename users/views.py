from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from products.models import Product 


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            # Send confirmation email
            current_site = get_current_site(request)
            subject = 'Registration Confirmation'
            message = render_to_string('confirmation_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            user_email = request.POST.get("email")
            email=EmailMessage(subject, message,to=[user_email])
            email.content_subtype = "html" # this is the crucial part 
            email.send()           
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard or any desired page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('dashboard')  # Redirect to dashboard or any desired page
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html'
            )
            user_email=request.POST.get("email")
            message = render_to_string('password_reset_email.html', {
                'user': user_email
            })
            email = EmailMessage('Reset your Heathy Basket Account Password !!!', message, to=[user_email])
            email.content_subtype = "html" # this is the crucial part 
            email.send()
            messages.info(request, 'Password reset email sent!')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})

@login_required
def dashboard(request):
    products = Product.objects.all()  # Retrieve all products from the database

    return render(request, 'dashboard.html', {'products': products})