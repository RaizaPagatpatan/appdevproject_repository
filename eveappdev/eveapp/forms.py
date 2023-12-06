from django import forms
from .models import Account, Event
from django.apps import apps
from multiupload.fields import MultiFileField


Organization = apps.get_model('CreateAccount', 'Organization')
Student = apps.get_model('CreateAccount', 'Student')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class OrgRegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput, label="Email")
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    user_type = forms.CharField(widget=forms.HiddenInput, initial='O')
    organization_name = forms.CharField(widget=forms.TextInput, label="Organization Name")

    class Meta:
        model = Organization
        fields = ['email', 'username', 'password', 'user_type', 'organization_name']


class StudentRegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput, label="Email")
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    first_name = forms.CharField(widget=forms.TextInput, label="Firstname")
    last_name = forms.CharField(widget=forms.TextInput, label="Lastname")
    user_type = forms.CharField(widget=forms.HiddenInput, initial='S')

    class Meta:
        model = Student
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'user_type']

class Verification(forms.ModelForm):

    # org_Name = forms.CharField(max_length=100, label="Organization Name")
    orgName = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=forms.HiddenInput,
        required=False
    )
    nameApplicant = forms.CharField(max_length=150, label="Name of Applicant")
    email = forms.EmailField(max_length=250)
    details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Applicant Details")
    account_status = forms.CharField(
        widget=forms.HiddenInput,
        initial='P')
    upload_file = forms.FileField(label="Upload Accreditation Certificate")
    class Meta:
        model = Account
        fields = [ 'orgName', 'nameApplicant' , 'email', 'details', 'account_status', 'upload_file']



class EventForm(forms.ModelForm):
    eventName = forms.CharField(max_length=100, label="Event Name")
    organizer = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=forms.HiddenInput,
    )
    details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Event Details")
    start = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), label="Start Date and Time")
    end = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), label="End Date and Time")
    location = forms.CharField(max_length=100, label="Location")
    images = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, label="Event Images", required=False)

    class Meta:
        model = Event
        fields = ['eventName', 'organizer', 'details', 'start', 'end', 'location', 'images']


class OrganizerFilterForm(forms.Form):
    organizer = forms.ModelChoiceField(queryset=Organization.objects.all(), empty_label="Select Organizer", required=False)
    eventName = forms.CharField(max_length=100, required=False)
    date_filter = forms.ChoiceField(choices=[
        ('', 'Select Date Filter'),
        ('this_month', 'This Month'),
        ('next_month', 'Next Month'),
        ('this_week', 'This Week'),
        ('today', 'Today'),
        ('ongoing', 'Ongoing Events'),
        ('finished', 'Finished Events'),
    ], required=False)