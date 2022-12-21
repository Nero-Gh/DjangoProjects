from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from .utils import token_generator

from django.contrib import auth
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.

class UserValidationView(View):
    
    def post(self,request):

        # this takes data from the FORM body
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({"username_error":"Username should only contain alpha numeric characters!"}, status = 400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"Sorry username already exit, choose a new one."}, status = 409)

        return JsonResponse({"Username":True})

class EmailValidationView(View):
    
    def post(self,request):

        # this takes data from the FORM body
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({"email_error":"Email is invalid."}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error":"Sorry email already exit, choose a new one."}, status = 409)

        return JsonResponse({"Email":True})
       


class RegistrationView(View):
    
    def get(self,request):
        return render(request,'authentication/register.html')

    def post(self,request):

        # get user details
        username =request.POST['username']
        email =request.POST['email']
        password =request.POST['password']

        context = {
            "fieldvalues":request.POST
        }

        # validate user
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request,"Password too short. Try Again😥")
                    return render(request,'authentication/register.html',context)
                #  create user account
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                # This is to disable user account
                user.is_active =False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

                activate_url = 'http://'+domain+link
                email_subject = "Activate your account."
                email_body = "Hi "+ user.username + ", Please use this link to verify your account 😊.\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@expense.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request,"Account created successfully 😉.")
                return render(request,'authentication/register.html')

        return render(request,'authentication/register.html')


class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                return redirect("login"+"?message="+"User already activated😑.")

            if user.is_active:
                return redirect('login')
            user.is_active=True
            user.save()
            return redirect('login')

            messages.success(request,"Account activated successfully😊.")
        except Exception as ex:
            pass
        return redirect('login')


class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')

    def post(self,request):

        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome, '+ user.username + ' you are now logged in 😉.')
                    return redirect('expenses')

                messages.error(request,'Account is not active, please check your email 📧.')
                return render(request,'authentication/login.html')

            messages.error(request,'Invalid credentials, please try again 😥.')
            return render(request,'authentication/login.html')
            
        messages.error(request,'Please fill all fields.')
        return render(request,'authentication/login.html')



class LogoutView(View):

    def post(self,request):
        auth.logout(request)
        messages.success(request,"You have been logged out.")
        return redirect('login')
        



class RequestPassowrdEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')



    def post(self,request):
        
        email = request.POST['email']
        # current_site = get_current_site(request)
        # user = User.objects.filter(email=email)

        # context = {
        #     'values':request.POST
        # }

        # if not validate_email(email):
        #     messages.error(request,'Please enter a valid email😑')
        #     return render(request,'authentication/reset-password.html',context)

        
        # if user.exists():
        #     email_contents={
        #         'user':user[0],
        #         'domain':current_site.domain,
        #         'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
        #         'token': PasswordResetTokenGenerator( ).make_token(user)
        #     }
        # # domain = get_current_site(request).domain
        # link = reverse('reset-user-password', kwargs={'uid':email_contents['uid'],'token':email_contents['token']})
        # email_subject = "Password reset instructions."

        # reset_url = 'http://'+current_site+link
        # email_body = "Hi "+ user.username + ", Please use this link to reset your account passsword 😊.\n" + reset_url
        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     'noreply@expense.com',
        #     [email],
        # )

        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # domain = get_current_site(request).domain
        # link = reverse('reset-user-password', kwargs={'uidb64':uidb64,'token':PasswordResetTokenGenerator().make_token(user)})

        # reset_url = 'http://'+domain+link
        # email_subject = "Password reset instructions."
        # email_body = "Hi "+ user.username + ", Please use this link to reset your account password 😊.\n" + reset_url
        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     'noreply@expense.com',
        #     [email],
        # )
        # email.send(fail_silently=False)

        messages.success(request,'We have sent you and email to reset your password')

        return render(request,'authentication/reset-password.html')



class CompletedPasswordReset(View):
    def get(self,request,uidb64,token):

        return render(request,'authentication/set-newpassword.html')


    def get(self,request,uidb64,token):

        return render(request,'authentication/set-newpassword.html')
