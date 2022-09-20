from django.shortcuts import render, redirect, get_object_or_404
from product.models import Category
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from account.models import UserProfile, User
from django.contrib import messages
from django.contrib.auth import logout
from order.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from account.forms import UserForm, UserProfileForm, RegistrationForm

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def LOGIN(request):
    categorys = Category.objects.all()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.warning(request,"Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')

    context = {
        'categorys':categorys,
    }
    return render(request, 'accounts/login.html', context)




def REGISTER(request):
    categorys = Category.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()


            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it.')
            return redirect('register')
            
            
    else:
        form = RegistrationForm()

    context = {
        'categorys':categorys,
        'form':form
    }
    return render(request, 'accounts/register.html', context)



def LOGOUT(request):
    logout(request)
    return redirect('home')






@login_required(login_url = 'login')
def MY_ACCOUNT(request):
    categorys = Category.objects.all()

    context = {
        'categorys':categorys,
    }
    return render(request, 'accounts/my_account.html', context)







@login_required(login_url = 'login')
def MY_ORDERS(request):
    categorys = Category.objects.all()
    orders = Order.objects.filter(user=request.user).order_by('-id')

    context = {
        'categorys':categorys,
        'orders':orders
    }
    return render(request, 'accounts/my_orders.html', context)



@login_required(login_url = 'login')
def ORDERS_DETAIL(request, id):
    categorys = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderItem.objects.filter(order_id=id )

    context = {
        'categorys':categorys,
        'order':order,
        'orderitems':orderitems
    }
    return render(request, 'accounts/orders_detail.html', context)









@login_required(login_url = 'login')
def EDIT_PROFILE(request):
    categorys = Category.objects.all()

    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'categorys':categorys,
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'accounts/edit_profile.html', context)






@login_required(login_url='login')
def CHANGE_PASSWORD(request):
    categorys = Category.objects.all()

    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')

    context = {
        'categorys':categorys,
    }
    
    return render(request, 'accounts/change_password.html', context)








def ACTIVATE(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')



def FORGOT_PASSWORD(request):
    categorys = Category.objects.all()
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    context ={
        'categorys':categorys
    }
    return render(request, 'accounts/forgotPassword.html', context)






def RESETPASSWORD_VALIDATE(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')





def RESET_PASSWORD(request):
    categorys = Category.objects.all()
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        context ={
        'categorys':categorys
    }
        return render(request, 'accounts/resetPassword.html', context)


