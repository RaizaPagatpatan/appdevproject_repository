from django.contrib import messages
from django.shortcuts import render, redirect
from django.apps import apps #student
from django.views import View


from .forms import *
from .models import Account
# Create your views here.

Student = apps.get_model('CreateAccount','Student') #student
Admin = apps.get_model('CreateAccount','Admin')
Organization = apps.get_model('CreateAccount','Organization')


def home_view(request):
    return render(request, 'home.html')


def pricing(request):
    return render(request, 'pricing.html')


class RegisterStudent(View): #student
    template = 'signup_student.html'

    def get(self, request):
        register = StudentRegisterForm()
        return render(request, self.template, {'form': register})

    def post(self, request):
        register = StudentRegisterForm(request.POST)
        email = request.POST['email']
        message = 'Registration successful'
        try:
            Student.objects.get(email=email)
            message = 'Email is already taken.'
        except Student.DoesNotExist:
            register.save()
            return redirect('login')

        return render(request, self.template, {'form': register, 'error_message': message})


class RegisterOrg(View):
    template_name = 'signup_org.html'

    def get(self, request):
        register = OrgRegisterForm()
        return render(request, self.template_name, {'form': register})

    def post(self, request):
        register = OrgRegisterForm(request.POST)
        message = 'Registration successful'

        if register.is_valid():
            organization_name = request.POST['organization_name']

            try:
                Organization.objects.get(organization_name=organization_name)
                message = 'Organization name is already taken.'
            except Organization.DoesNotExist:
                register.save()
                return redirect('login')

        return render(request, self.template_name, {'form': register, 'error_message': message})


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form, 'error_message': None})

    def post(self, request):
        error_message = None

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = None

            try:
                user = Student.objects.get(username=username, password=password, user_type="S")
                request.session['type'] = "S"
                request.session['user_id'] = user.user_id
                request.session['username'] = user.first_name
                return redirect('login')
            except Student.DoesNotExist:
                pass

            if not user:
                try:
                    user = Organization.objects.get(username=username, password=password, user_type="O")
                    request.session['type'] = "O"
                    request.session['user_id'] = user.user_id
                    request.session['username'] = user.organization_name
                    return redirect('login')
                except Organization.DoesNotExist:
                    pass

            if not user:
                try:
                    user = Admin.objects.get(username=username, password=password, user_type="A")
                except Admin.DoesNotExist:
                    pass

            if user:
                return redirect('login')
            else:
                error_message = "Invalid username or password."

        return render(request, self.template_name, {'form': form, 'error_message': error_message})
