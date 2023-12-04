from django.contrib import messages
from django.http import HttpResponse
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


# class LoginView(View):
#     template_name = 'login.html'
#
#     def get(self, request):
#         form = LoginForm()
#         return render(request, self.template_name, {'form': form, 'error_message': None})
#
#     def post(self, request):
#         error_message = None
#
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#
#             user = None
#
#             try:
#                 user = Student.objects.get(username=username, password=password, user_type="S")
#                 request.session['type'] = "S"
#                 request.session['user_id'] = user.user_id
#                 request.session['username'] = user.first_name
#                 return redirect('student_home')
#             except Student.DoesNotExist:
#                 pass
#
#             if not user:
#                 try:
#                     user = Organization.objects.get(username=username, password=password, user_type="O")
#                     request.session['type'] = "O"
#                     request.session['user_id'] = user.user_id
#                     request.session['username'] = user.organization_name
#                     return redirect('org_home')
#                 except Organization.DoesNotExist:
#                     pass
#
#             if not user:
#                 try:
#                     user = Admin.objects.get(username=username, password=password, user_type="A")
#                 except Admin.DoesNotExist:
#                     pass
#
#             if user:
#                 return redirect('student_home')
#             else:
#                 error_message = "Invalid username or password."
#
#         return render(request, self.template_name, {'form': form, 'error_message': error_message})
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
                return redirect('student_home')
            except Student.DoesNotExist:
                pass

            if not user:
                try:
                    user = Organization.objects.get(username=username, password=password, user_type="O")
                    request.session['type'] = "O"
                    request.session['user_id'] = user.user_id
                    request.session['username'] = user.organization_name
                    return redirect('org_home')
                except Organization.DoesNotExist:
                    pass

            if not user:
                try:
                    user = Admin.objects.get(username=username, password=password, user_type="A")
                except Admin.DoesNotExist:
                    pass

            if user:
                return redirect('student_home')
            else:
                error_message = "Invalid username or password."

        return render(request, self.template_name, {'form': form, 'error_message': error_message})


class OrgHome(View):
    template_name = 'org_home.html'

    def get(self, request):
        user = request.session['user_id']
        username = request.session['username']
        # events = Event.objects.filter(organizer=user).values()  'events': events,

        return render(request, self.template_name, { 'username': username})


class ShowStudentHome(View):
    # def get(self, request):
    #     return HttpResponse("Student Home Page")
    template = 'student_home.html'

    def get(self, request):
        username = request.session['username']
        # events = Event.objects.all() ++++++ 'events': events,
        return render(request, self.template, {'username': username})


class Verify(View):
    def post(self, request):
        form = Verification(request.POST)
        if form.is_valid():
            form.save()
            return redirect('verify_home')

    def get(self, request):
        form = Verification(initial={'orgName': request.session['user_id']})
        return render(request, 'verification_page.html', {'form': form})


class OrgVerifyView(View):
    template_name = 'verify_home.html'

    def get(self, request):
        user = request.session['user_id']
        username = request.session['username']
        # events = Event.objects.filter(organizer=user).values()
        org_lists = Account.objects.filter(orgName=user).values()
        return render(request, self.template_name, {'org_lists': org_lists, 'username' : username})


class OrgList(View):
    template_name = 'org_list.html'

    def get(self, request):
        user = request.session['user_id']
        username = request.session['username']
        # events = Event.objects.filter(organizer=user).values()  'events': events,
        # org_lists = Account.objects.filter(orgName=user).values() 'org_lists': org_lists,
        return render(request, self.template_name, {'username': username})
