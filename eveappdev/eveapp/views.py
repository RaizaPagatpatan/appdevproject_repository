from django.contrib import messages
from django.db import IntegrityError
from django.db.models.functions import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps #student
from django.urls import reverse
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


# def custom_404(request, exception):
#     return render(request, 'student_404.html', status=404)

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
    template_name = 'about.html'

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

class AboutUs(View):
    template_name = 'aboutus.html'

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
        message = 'Registration successful'

        # Modified register: I made the email and username unique in models.py and
        # handled duplicate error through IntegrityError instead  - lyra
        try:
            if register.is_valid():
                register.save()
                return redirect('login')
        except IntegrityError:
            # Handle the case where email or username is not unique
            return render(request, self.template, {'error': 'Email or username already exists'})

        # OLD CODE
        # email = request.POST['email']
        # try:
        #     Student.objects.get(email=email)
        #     message = 'Email is already taken.'
        # except Student.DoesNotExist:
        #     register.save()
        #     return redirect('login')

        return render(request, self.template, {'form': register, 'message': message})


class RegisterOrg(View):
    template_name = 'signup_org.html'

    def get(self, request):
        register = OrgRegisterForm()
        return render(request, self.template_name, {'form': register})

    def post(self, request):
        register = OrgRegisterForm(request.POST)
        message = 'Registration successful'

        # Modified register: I made the email and username unique in models.py and
        # handled duplicate error through IntegrityError instead  - lyra
        try:
            if register.is_valid():
                register.save()
                return redirect('login')
        except IntegrityError:
            # Handle the case where email or username is not unique
            return render(request, self.template_name, {'error': 'Email or username already exists'})

        # OLD CODE
        # if register.is_valid():
        #     organization_name = request.POST['organization_name']
        #     org_email = request.POST['email']
        # try:
        #     Organization.objects.get(organization_name=organization_name, email=org_email)
        #     message = 'Organization name and email is already taken.'
        # except Organization.DoesNotExist:
        #     register.save()
        #     return redirect('login')

        return render(request, self.template_name, {'form': register, 'message': message})


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


class OrgAnnouncementsList(View):
    template = 'org_announcements_list.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']
            username = request.session['username']
            user_type = request.session.get('type', None)

            if user_type == "O":
                text_posts = TextPost.objects.filter(organization=user)

                # Iterate over org_lists and add profile_pic to each organization
                for tp in text_posts:
                    try:
                        # Try to get the profile associated with the organization
                        profile = Profile.objects.get(organization=user)
                        org = Organization.objects.get(organization_name=username)

                        # Assign the profile_pic to the org_lists object
                        tp.org_name = org.organization_name
                        tp.profile_pic = profile.profile_pic

                    except Profile.DoesNotExist:
                        # Handle the case where there is no profile for the organization
                        tp.profile_pic = None

                return render(request, self.template, {'text_posts': text_posts})
            else:
                return redirect('student_home')
        else:
            return redirect('login')

    def post(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            if user_type == "O":
                if 'delete_textpost_id' in request.POST:
                    textpost_id = request.POST['delete_textpost_id']
                    textpost = get_object_or_404(TextPost, pk=textpost_id, organization=request.session['user_id'])
                    textpost.delete_textpost()

                # redirect after delete
                return redirect('org_announce_list')
            else:
                return redirect('student_home')
        else:
            return redirect('login')


class EditTextPost(View):
    template = 'edit_announcement.html'

    def get(self, request, textpost_id):
        if 'user_id' in request.session and 'username' in request.session:
            o_user = request.session['user_id']
            user_type = request.session.get('type', None)

            if user_type == "O":
                textpost = get_object_or_404(TextPost, pk=textpost_id, organization=o_user)
                form = TextPostForm(instance=textpost)
                return render(request, self.template, {'form': form, 'textpost': textpost})
            else:
                return redirect('student_home')

        else:
            return redirect('login')

    def post(self, request, textpost_id):
        if 'user_id' in request.session and 'username' in request.session:
            o_user = request.session['user_id']
            user_type = request.session.get('type', None)

            if user_type == "O":
                textpost = get_object_or_404(TextPost, pk=textpost_id, organization=o_user)
                form = TextPostForm(request.POST, instance=textpost)

                if form.is_valid():
                    form.save()
                    return redirect('org_announce_list')
                else:
                    error_messages = form.errors.values()
                    for message in error_messages:
                        messages.error(request, message)

                    return redirect('edit_text_post', textpost_id=textpost_id)
            else:
                return redirect('student_home')
        else:
            return redirect('login')


class CreateTextPost(View):
    template = 'create_text_post.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            form = TextPostForm(initial={'organization': request.session['user_id']})

            if user_type == "O":
                return render(request, self.template, {'form': form})
            else:
                return redirect('student_home')

        else:
            return redirect('login')

    def post(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            form = TextPostForm(request.POST)

            if user_type == "O":
                if form.is_valid():
                    text_post = form.save()

                    # Notify followers of the organization
                    self.notify_followers(text_post.organization, text_post)

                    return redirect('org_announce_list')
            else:
                return redirect('student_home')
        else:
            return redirect('login')

    def notify_followers(self, organization, text_post):
        followers = organization.followers.all()

        for follower in followers:
            notification = StudentNotification(
                student_user=follower.follower,
                message=f"The organization {organization.organization_name} has made a new post: {text_post.content[:8]}....",
                post=text_post,  # Associate the post with the notification
            )
            notification.save()


class StudentViewAnnouncements(View):
    template = "student_view_announcements.html"

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            s_user = request.session['user_id']
            username = request.session['username']
            user_type = request.session.get('type', None)

            if user_type == "S":
                student = Student.objects.get(pk=s_user)
                followed_orgs = Follow.objects.filter(follower=student).values_list('organization', flat=True)
                custom_tp = TextPost.objects.filter(organization__in=followed_orgs)

                # filter
                form = TextPostFilterForm(request.GET)

                if form.is_valid():
                    organizer_id = form.cleaned_data.get('organizer')

                    if organizer_id:
                        custom_tp = custom_tp.filter(organization=organizer_id)

                for ct in custom_tp:
                    try:
                        profile = Profile.objects.get(organization=ct.organization)
                        ct.profile_pic = profile.profile_pic
                    except Profile.DoesNotExist:
                        # Handle the case where there is no profile for the organization
                        ct.profile_pic = None

                return render(request, self.template,{'username':username,'text_posts':custom_tp,'form':form})
            else:
                return redirect('org_home')
        else:
            redirect('login')


class ShowStudentHome(View):
    template_name = 'student_home.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            s_user = request.session['user_id']
            username = request.session['username']
            user_type = request.session.get('type', None)

            if user_type == "S":
                events = Event.objects.all()
                student = Student.objects.get(pk=s_user)
                followed_orgs = Follow.objects.filter(follower=student).values_list('organization', flat=True)
                custom_events = Event.objects.filter(organizer__in=followed_orgs)
                now = timezone.now()

                for ce in custom_events:
                    try:
                        profile = Profile.objects.get(organization=ce.organizer)
                        ce.profile_pic = profile.profile_pic
                    except Profile.DoesNotExist:
                        # Handle the case where there is no profile for the organization
                        ce.profile_pic = None

                custom_tp = TextPost.objects.filter(organization__in=followed_orgs)

                for ct in custom_tp:
                    try:
                        profile = Profile.objects.get(organization=ct.organization)
                        ct.profile_pic = profile.profile_pic
                    except Profile.DoesNotExist:
                        # Handle the case where there is no profile for the organization
                        ct.profile_pic = None

                bookmarks = Bookmark.objects.filter(student_user=s_user)[:10]

                context = {
                    'username': username,
                    'bookmarks': bookmarks,
                    'custom_events': custom_events,
                    'events': events,
                    'text_posts': custom_tp,
                    'now': now,
                }
                return render(request, self.template_name, context)
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
                follow = Follow.objects.create(follower=curr_student, organization=organization)

                self.notify_org(organization, curr_student, follow)

            return redirect('org_profile', org_id=org_id)
        else:
            return redirect('login')

    def notify_org(self, organization, curr_student, follow):
            notification = OrgNotification(
                org_user=organization,
                message=f'{curr_student.username} started following your organization.',
                followed=follow,
            )
            notification.save()

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
                follow = Follow.objects.create(follower=curr_student, organization=organization)

                self.notify_org(organization, curr_student, follow)

            return redirect('org_list')
        else:
            return redirect('login')

    def notify_org(self, organization, curr_student, follow):
            notification = OrgNotification(
                org_user=organization,
                message=f'{curr_student.username} started following your organization.',
                followed=follow,
            )
            notification.save()


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


class BookmarkEventView(View):
    def post(self, request, event_id):
        # Check if the user is authenticated
        if 'user_id' in request.session and 'username' in request.session:
            user_id = request.session['user_id']
            event = get_object_or_404(Event, pk=event_id)
            s_user = get_object_or_404(Student, pk=user_id)

            # Check if the user has already bookmarked the event
            bookmark_exists = Bookmark.objects.filter(student_user=s_user, event=event).exists()

            if not bookmark_exists:
                Bookmark.objects.create(student_user=s_user, event=event)

            # Redirect to the previous page or a default URL if the referrer is not available
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'student_event_view'))
        else:
            return redirect('login')


class RemoveBookmarkEventView(View):
    def post(self, request, event_id):
        # Check if the user is authenticated
        if 'user_id' in request.session and 'username' in request.session:
            user_id = request.session['user_id']
            event = get_object_or_404(Event, pk=event_id)
            s_user = get_object_or_404(Student, pk=user_id)

            # Check if the user has already bookmarked the event
            bookmark_exists = Bookmark.objects.filter(student_user=s_user, event=event).exists()

            if bookmark_exists:
                # Remove the bookmark
                Bookmark.objects.filter(student_user=s_user, event=event).delete()

            # Redirect to the previous page or a default URL if the referrer is not available
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'student_event_view'))
        else:
            return redirect('login')


class RSVPYes(View):

    def post(self, request, org_id, event_id):
        if 'user_id' in request.session and 'username' in request.session:
            s_user = request.session['user_id']
            user_type = request.session.get('type', None)
            user = request.session['user_id']
            curr_student = Student.objects.get(pk=user)

            if user_type == "S":
                event = get_object_or_404(Event, pk=event_id)
                organization = get_object_or_404(Organization, pk=org_id)

                if not event.rsvp_yes.filter(user_id=s_user).exists():
                    rsvpd = RSVP.objects.create(student=curr_student, event=event)

                    OrgNotification.objects.create(
                        org_user=organization,
                        message=f'Student {curr_student.username} RSVPed "Yes" to your event "{event.eventName}".',
                        rsvped=rsvpd)

                if event.rsvp_no.filter(user_id=s_user).exists():
                    event.rsvp_no.remove(s_user)

                return JsonResponse({'message': 'RSVP successful'})
            else:
                return redirect('org_home')
        else:
            return redirect('login')




class RSVPNo(View):

    def post(self, request, event_id):
        if 'user_id' in request.session and 'username' in request.session:
            s_user = request.session['user_id']
            user_type = request.session.get('type', None)

            if user_type == "S":
                event = get_object_or_404(Event, pk=event_id)

                if not event.rsvp_no.filter(user_id=s_user).exists():
                    event.rsvp_no.add(s_user)
                if event.rsvp_yes.filter(user_id=s_user).exists():
                    event.rsvp_yes.remove(s_user)

                return JsonResponse({'message': 'RSVP successful'})
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'student_event_view'))
            else:
                return redirect('org_home')
        else:
            return redirect('login')


class PostDetailView(View):
    template = 'post_detail.html'

    def get(self, request, textpost_id):
        if 'user_id' in request.session and 'username' in request.session:
            username = request.session['username']
            user_type = request.session.get('type', None)

            if user_type == "S":
                text_post = get_object_or_404(TextPost, id=textpost_id)

                try:
                    profile = Profile.objects.get(organization=text_post.organization)
                    text_post.profile_pic = profile.profile_pic
                except Profile.DoesNotExist:
                    # Handle the case where there is no profile for the organization
                    text_post.profile_pic = None

                return render(request, self.template, {'text_post': text_post, 'username': username})
            else:
                return redirect('org_home')

        else:
            return redirect('login')


class NEventDetailView(View):
    template = "student_view_event_detail.html"

    def get(self, request, event_id):
        if 'user_id' in request.session and 'username' in request.session:
            username = request.session['username']
            user_type = request.session.get('type', None)

            if user_type == "S":
                now = timezone.now()
                try:
                    event = get_object_or_404(Event, eventID=event_id)
                except Http404:
                    # Handle the 404 error here (e.g., redirect to a custom error page)
                    return render(request, 'student_404.html', {'username': username})

                try:
                    profile = Profile.objects.get(organization=event.organizer)
                    event.profile_pic = profile.profile_pic
                except Profile.DoesNotExist:
                    # Handle the case where there is no profile for the organization
                    event.profile_pic = None

                return render(request, self.template, {'event': event, 'username': username, 'now': now})
            else:
                return redirect('org_home')

        else:
            return redirect('login')


class StudentBookmarksView(View):
    template = 'student_bookmark_view.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            s_user = request.session['user_id']
            username = request.session['username']
            user_type = request.session.get('type', None)
            now = timezone.now()

            if user_type == "S":
                student = Student.objects.get(pk=s_user)
                events = Event.objects.filter(event_bookmarks__student_user=student) #bookmarked events

                form = OrganizerFilterForm(request.GET)  # Bind the form to the request data

                if form.is_valid():
                    organizer_id = form.cleaned_data.get('organizer')
                    event_name = form.cleaned_data.get('eventName')  # Corrected to match the form field name
                    date_filter = form.cleaned_data.get('date_filter')

                    if organizer_id:
                        events = events.filter(organizer_id=organizer_id)

                    if event_name:
                        events = events.filter(
                            eventName__icontains=event_name)  # Corrected to match the model field name

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

                return render(request, self.template, {'events': events, 'username': username, 'form': form, 'now': now})
            else:
                return redirect('org_home')

        else:
            return redirect('login')


class StudentRSVPSView(View):
    template = 'student_rsvps_view.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            s_user = request.session['user_id']
            username = request.session['username']
            user_type = request.session.get('type', None)
            now = timezone.now()

            if user_type == "S":
                student = Student.objects.get(pk=s_user)
                events = Event.objects.filter(rsvped_events__student=student) #RSVP'd events

                form = OrganizerFilterForm(request.GET)  # Bind the form to the request data

                if form.is_valid():
                    organizer_id = form.cleaned_data.get('organizer')
                    event_name = form.cleaned_data.get('eventName')  # Corrected to match the form field name
                    date_filter = form.cleaned_data.get('date_filter')

                    if organizer_id:
                        events = events.filter(organizer_id=organizer_id)

                    if event_name:
                        events = events.filter(
                            eventName__icontains=event_name)  # Corrected to match the model field name

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

                return render(request, self.template, {'events': events, 'username': username, 'form': form, 'now': now})
            else:
                return redirect('org_home')

        else:
            return redirect('login')


class MarkOneAsRead(View):

    def post(self, request, notification_id):
        if 'user_id' in request.session and 'username' in request.session:
            user = request.session['user_id']

            user_type = request.session.get('type', None)

            if user_type == "O":
                notification = get_object_or_404(OrgNotification, id=notification_id)
                notification.is_read = True
                notification.save()

                return JsonResponse({'status': 'success'})
            elif user_type == "S":
                notification = get_object_or_404(StudentNotification, id=notification_id)
                notification.is_read = True
                notification.save()

                # Redirect to the associated post
                # if notification.post:
                #     return redirect('post_detail', textpost_id=notification.post.id)
                # else:
                #     # Handle the case where the post is not available
                #     return HttpResponse("Post not found.")
                # Return the post ID in the JSON response
                return JsonResponse(
                    {'status': 'success', 'post_id': notification.post.id if notification.post else None})

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
            username = request.session['username']
            student_id = request.session['user_id']
            user_type = request.session.get('type', None)

            if user_type == "S":
                student_notifications = StudentNotification.objects.filter(student_user=student_id)[
                                    :50]  # only shows a max of 50 notifs

                # Render the template with the notifications
                return render(request, self.template, {'username': username, 'notifications': student_notifications})
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

        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            form = EventForm(request.POST, request.FILES)

            if user_type == "O":
                error_messages = "You are not Verified!"
                if form.is_valid():
                    event = form.save()

                    # Notify followers of the organization
                    self.notify_followers(event.organizer, event)

                    return redirect('org_event_list')
                else:
                    error_messages = form.errors.values()
                    for message in error_messages:
                        messages.error(request, message)

                    return render(request, 'add_event.html', {'form': form, 'error_message': error_messages})
            else:
                return redirect('student_home')

        else:
            return redirect('login')

    def notify_followers(self, organization, event):
        followers = organization.followers.all()

        for follower in followers:
            notification = StudentNotification(
                student_user=follower.follower,
                message=f"The organization {organization.organization_name} has a new event! {event.eventName}: {event.details[:8]}....",
                event_n=event,  # Associate the post with the notification
            )
            notification.save()

    def get(self, request):
        form = EventForm(initial={'organizer': request.session['user_id']})
        return render(request, 'add_event.html', {'form': form})


class OrgDashboardView(View):
    template = 'org_dashboard.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            if user_type == 'O':
                data = self.get_last_28_days_data(request)

                context = {
                    'bookmarks_count': data['bookmarks_count'],
                    'rsvps_count': data['rsvps_count'],
                    'follows_count': data['follows_count'],
                }

                return render(request, self.template, context)
            else:
                return redirect('student_home')
        else:
            return redirect('login')

    def get_last_28_days_data(self, request):
        # Calculate the date 28 days ago from today
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=28)

        o_user = request.session['user_id']

        events_made = Event.objects.filter(organizer=o_user)

        # Count bookmarks in the last 28 days
        bookmarks_count = Bookmark.objects.filter(event__in=events_made, created_at__range=[start_date, end_date]).count()

        # Count RSVPs in the last 28 days
        rsvps_count = RSVP.objects.filter(event__in=events_made, timestamp__range=[start_date, end_date]).count()

        # Count follows in the last 28 days
        follows_count = Follow.objects.filter(organization=o_user, timestamp__range=[start_date, end_date]).count()

        return {
            'bookmarks_count': bookmarks_count,
            'rsvps_count': rsvps_count,
            'follows_count': follows_count,
        }


class OrgDashboardFollowersView(View):
    template = 'org_dashboard_followers.html'

    def get(self, request):
        if 'user_id' in request.session and 'username' in request.session:
            o_user = request.session['user_id']
            user_type = request.session.get('type', None)

            if user_type == 'O':
                followers_count = Follow.objects.filter(organization=o_user).count()

                return render(request, self.template, {'followers_count': followers_count})
            else:
                return redirect('student_home')
        else:
            return redirect('login')


class OrgViewRSVPCount(View):
    template = 'org_view_rsvps.html'

    def get(self, request, event_id):
        if 'user_id' in request.session and 'username' in request.session:
            user_type = request.session.get('type', None)

            if user_type == 'O':
                event = get_object_or_404(Event, pk=event_id)

                # Get RSVP counts
                going_count = event.rsvp_yes.count()
                not_going_count = event.rsvp_no.count()

                # Get name of attendees
                attendees = RSVP.objects.filter(event_id=event_id)

                for attendee in attendees:
                    attendee.name = f"{attendee.student.last_name}, {attendee.student.first_name}"
                    attendee.email = attendee.student.email

                context = {
                    'event': event,
                    'going_count': going_count,
                    'not_going_count': not_going_count,
                    'attendees': attendees,
                }

                return render(request, self.template, context)
            else:
                return redirect('student_home')
        else:
            return redirect('login')


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
        now = timezone.now()

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

        return render(request, self.template, {'events': events, 'username': username, 'form': form, 'now': now})
