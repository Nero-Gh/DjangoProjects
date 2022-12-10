from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from .utils import token_generator


from django.urls import reverse
from django.utils.encoding import force_bytes, force_str , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


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

        
