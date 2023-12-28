from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps #student
from django.views import View
from django.contrib.auth import logout
from .forms import *
from .models import Account
from datetime import date, timedelta
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import *

# Create your views here.

Student = apps.get_model('CreateAccount','Student') #student
Admin = apps.get_model('CreateAccount','Admin')
Organization = apps.get_model('CreateAccount','Organization')


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_id = request.session['user_id']
            username = request.session['username']

            # Assuming you have stored the user type in the session
            user_type = request.session.get('type', None)

            if user_type == "S":
                return redirect('student_home')  # Redirect to the student home view
            elif user_type == "O":
                return redirect('org_home')

        else:
            return render(request, self.template_name)


class Services(View):
    template_name = 'services.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_id = request.session['user_id']
            username = request.session['username']

            # Assuming you have stored the user type in the session
            user_type = request.session.get('type', None)

            if user_type == "S":
                return redirect('student_home')  # Redirect to the student home view
            elif user_type == "O":
                return redirect('org_home')

        else:
            return render(request, self.template_name)


def pricing(request):
    return render(request, 'pricing.html')


def pricing_org(request):
    return render(request, 'pricing_org.html')


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
            org_email = request.POST['email']


            try:
                Organization.objects.get(organization_name=organization_name, email=org_email)
                message = 'Organization name and email is already taken.'
            except Organization.DoesNotExist:
                register.save()
                return redirect('login')

        return render(request, self.template_name, {'form': register, 'error_message': message})


class Logout(View):
    def get(self, request):
        if 'type' in request.session:
            del request.session['type']
        if 'user_id' in request.session:
            del request.session['user_id']
        if 'username' in request.session:
            del request.session['username']

        return redirect('home_view')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            if user_type == "S":
                return redirect('student_home')
            elif user_type == "O":
                return redirect('org_home')

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
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            username = request.session['username']
            user_type = request.session.get('type', None)

            try:
                profile = Profile.objects.get(organization_id=user)
            except Profile.DoesNotExist:
                # Handle the case where the profile does not exist
                profile = None

            if user_type == "O":
                return render(request, self.template_name, {'profile': profile, 'username': username})
            else:
                return redirect('student_home')
        else:
            return redirect('login')


class UpdateProfile(View):
    template = "edit_profile.html"
    def post(self, request):
        try:
            # Try to get the existing profile instance
            profile_instance = Profile.objects.get(organization=request.session['user_id'])
        except Profile.DoesNotExist:
            # If the profile does not exist, handle it appropriately
            # For example, you can create a new profile instance
            profile_instance = None

        form = ProfileForm(request.POST, request.FILES, instance=profile_instance)

        error_messages = "You are not Verified!"
        if form.is_valid():
            form.save()
            return redirect('org_home')
        else:
            error_messages = form.errors.values()
            for message in error_messages:
                messages.error(request, message)

            return redirect('update_profile')

    def get(self, request):
        try:
            profile_instance = Profile.objects.get(organization=request.session['user_id'])
        except Profile.DoesNotExist:
            # Handle the case where the profile does not exist
            profile_instance = None

        form = ProfileForm(initial={'organization': request.session['user_id']}, instance=profile_instance)
        return render(request, 'edit_profile.html', {'form': form})


class ShowStudentHome(View):
    template_name = 'student_home.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            username = request.session['username']

            user_type = request.session.get('type', None)

            if user_type == "S":
                return render(request, self.template_name, {'username': username})
            else:
                return redirect('org_home')
        else:
            return redirect('login')


def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class Verify(View):
    def post(self, request):
        form = Verification(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('verify_home')
        return render(request, 'verification_page.html', {'form': form, 'error_message': "Form invalid. Try again."})

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
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            username = request.session['username']

            user_type = request.session.get('type', None)
            # allow approved by admin only
            org_lists = Account.objects.filter(account_status='A')

            # Iterate over org_lists and add profile_pic to each organization
            for org in org_lists:
                try:
                    # Try to get the profile associated with the organization
                    profile = Profile.objects.get(organization=org.orgName.user_id)
                    # Assign the profile_pic to the org_lists object
                    org.profile_pic = profile.profile_pic
                except Profile.DoesNotExist:
                    # Handle the case where there is no profile for the organization
                    org.profile_pic = None

            if user_type == "S":
                return render(request, self.template_name, {'username': username, 'org_lists': org_lists})
            else:
                return redirect('org_home')
        else:
            return redirect('login')

        # user = request.session['user_id']
        # username = request.session['username']
        #
        # # allow approved by admin only
        # org_lists = Account.objects.filter(account_status='A')
        #
        # return render(request, self.template_name, {'username': username, 'org_lists': org_lists})


class ProfileView(View):
    template = 'student_viewOrgProfile.html'

    def get(self, request, org_id):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            username = request.session['username']

            user_type = request.session.get('type', None)

            # Use get_object_or_404 to handle the case where the organization doesn't exist
            organization = get_object_or_404(Organization, pk=org_id)

            try:
                org_profile = Profile.objects.get(organization=organization)
            except Profile.DoesNotExist:
                # Handle the case where the profile does not exist
                org_profile = None

            # Now, query the Profile using the organization instance


            if user_type == "S":
                return render(request, self.template, {'username': username, 'org_profile': org_profile})
            else:
                return redirect('org_home')
        else:
            return redirect('login')


class FollowOrganizationView(View):
    def post(self, request, org_id):
        organization = Organization.objects.get(pk=org_id)

        # Check if the user is authenticated
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']

            curr_student = Student.objects.get(pk=user)

            # Check if the user is not already following the organization
            if not curr_student.following.filter(organization=organization).exists():
                Follow.objects.create(follower=curr_student, organization=organization)

                # Create a notification for the organization
                OrgNotification.objects.create(
                    org_user=organization,  #org_user field from the OrgNotification model
                    message=f'{curr_student.username} started following your organization.',
                )

            return redirect('org_profile', org_id=org_id)
        else:
            return redirect('login')

class UnfollowOrganizationView(View):
    def post(self, request, org_id):
        organization = Organization.objects.get(pk=org_id)

        # Check if the user is authenticated
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            # Check if the user is following the organization
            curr_student = Student.objects.get(pk=user)
            follow_instance = curr_student.following.filter(organization=organization).first()
            if follow_instance:
                follow_instance.delete()

            return redirect('org_profile', org_id=org_id)
        else:
            return redirect('login')



class FollowOrgListView(View):
    def post(self, request, org_id):
        organization = Organization.objects.get(pk=org_id)

        # Check if the user is authenticated
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']

            curr_student = Student.objects.get(pk=user)

            # Check if the user is not already following the organization
            if not curr_student.following.filter(organization=organization).exists():
                Follow.objects.create(follower=curr_student, organization=organization)

                # Create a notification for the organization
                OrgNotification.objects.create(
                    org_user=organization,  # org_user field from the OrgNotification model
                    message=f'{curr_student.username} started following your organization.',
                )

            return redirect('org_list')
        else:
            return redirect('login')

class UnfollowOrgListView(View):
    def post(self, request, org_id):
        organization = Organization.objects.get(pk=org_id)

        # Check if the user is authenticated
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            # Check if the user is following the organization
            curr_student = Student.objects.get(pk=user)
            follow_instance = curr_student.following.filter(organization=organization).first()
            if follow_instance:
                follow_instance.delete()

            return redirect('org_list')
        else:
            return redirect('login')

class MarkOneAsRead(View):

    def post(self, request, notification_id):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']

            user_type = request.session.get('type', None)

            if user_type == "O":
                notification = OrgNotification.objects.get(pk=notification_id)
                notification.is_read = True
                notification.save()
            elif user_type == "S":
               pass

            return JsonResponse({'status': 'success'})
        else:
            return redirect('login')


class MarkAllAsRead(View):
    def post(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']

            user_type = request.session.get('type', None)

            if user_type == "O":
                o_notifs = OrgNotification.objects.filter(org_user=user, is_read=False)
                o_notifs.update(is_read=True)
                return redirect('org_notifications')
            elif user_type == "S":
                s_notifs = StudentNotification.objects.filter(student_user=user, is_read=False)
                s_notifs.update(is_read=True)
                return redirect('student_notifications')
        else:
            return redirect('login')


class StudentNotifView(View):
    template = 'student_notifs.html'
    def get(self,request):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            username = request.session['username']

            user_type = request.session.get('type', None)

            if user_type == "S":
                return render(request, self.template, {'username': username})
            else:
                return redirect('org_home')
        else:
            return redirect('login')


class OrgNotifView(View):
    template = 'org_notifs.html'
    def get(self,request):
        if 'user_id' in request.session and 'username' in request.session:
            org_id = request.session['user_id']
            user_type = request.session.get('type', None)

            if user_type == "O":
                org_notifications = OrgNotification.objects.filter(org_user=org_id)[:50] #only shows a max of 50 notifs

                # Render the template with the notifications
                return render(request, self.template, {'notifications': org_notifications})
            else:
                return redirect('student_home')
        else:
            return redirect('login')


class AddEvent(View):
    def post(self, request):

        form = EventForm(request.POST, request.FILES)
        error_messages = "You are not Verified!"
        if form.is_valid():
            form.save()
            return redirect('org_event_list')
        else:
            error_messages = form.errors.values()
            for message in error_messages:
                messages.error(request, message)

            return redirect('add_event')

    def get(self, request):
        form = EventForm(initial={'organizer': request.session['user_id']})
        return render(request, 'add_event.html', {'form': form})


class EditEvent(View):
    template_name = 'edit_event.html'

    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id, organizer=request.session['user_id'])
        form = EventForm(instance=event)
        return render(request, self.template_name, {'form': form, 'event': event})

    def post(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id, organizer=request.session['user_id'])
        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            form.save()
            return redirect('org_event_list')
        else:
            error_messages = form.errors.values()
            for message in error_messages:
                messages.error(request, message)

            return redirect('edit_event', event_id=event_id)


class OrgEventListView(View):
    template_name = 'org_eventList.html'

    def get(self, request):
        user = request.session['user_id']
        username = request.session['username']
        events = Event.objects.filter(organizer=user).values()
        return render(request, self.template_name, {'events': events, 'username': username})

    def post(self, request):
        if 'delete_event_id' in request.POST:
            event_id = request.POST['delete_event_id']
            event = get_object_or_404(Event, pk=event_id, organizer=request.session['user_id'])
            event.delete_event()

        #redirect after delete
        return redirect('org_event_list')


class EventStudentView(View):
    template = 'student_eventView.html'

    def get(self, request):
        username = request.session['username']
        events = Event.objects.all()
        form = OrganizerFilterForm(request.GET)  # Bind the form to the request data

        if form.is_valid():
            organizer_id = form.cleaned_data.get('organizer')
            event_name = form.cleaned_data.get('eventName')  # Corrected to match the form field name
            date_filter = form.cleaned_data.get('date_filter')

            if organizer_id:
                events = events.filter(organizer_id=organizer_id)

            if event_name:
                events = events.filter(eventName__icontains=event_name)  # Corrected to match the model field name

            if date_filter == 'this_month':
                start_date = date.today().replace(day=1)
                end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                events = events.filter(start__range=[start_date, end_date])

            if date_filter == 'next_month':
                start_date = date.today().replace(day=1) + timedelta(days=32)
                end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                events = events.filter(start__range=[start_date, end_date])

            elif date_filter == 'this_week':
                today = date.today()
                start_date = today - timedelta(days=today.weekday())
                end_date = start_date + timedelta(days=6)
                events = events.filter(start__range=[start_date, end_date])

            elif date_filter == 'today':
                today = date.today()
                events = events.filter(start__date=today)

            elif date_filter == 'ongoing':
                events = events.filter(start__lte=date.today(), end__gte=date.today())

            elif date_filter == 'finished':
                events = events.filter(end__lt=date.today())

        return render(request, self.template, {'events': events, 'username': username, 'form': form})
