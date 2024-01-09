from django import forms
from django.core.exceptions import ValidationError

from .models import Account, Event, Profile, TextPost, Follow
from django.apps import apps
from django.utils import timezone  # Import timezone module
from multiupload.fields import MultiFileField

Organization = apps.get_model('CreateAccount', 'Organization')
Student = apps.get_model('CreateAccount', 'Student')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")


class OrgRegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label="Email")
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")
    user_type = forms.CharField(widget=forms.HiddenInput, initial='O')
    organization_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Organization Name'}), label="Organization Name")

    class Meta:
        model = Organization
        fields = ['email', 'username', 'password', 'user_type', 'organization_name']


class StudentRegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label="Email")
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), label="Firstname")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), label="Lastname")
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
        fields = ['orgName', 'nameApplicant' , 'email', 'details', 'account_status', 'upload_file']


class EventForm(forms.ModelForm):
    eventName = forms.CharField(max_length=100, label="Event Name")
    organizer = forms.ModelChoiceField(
        queryset=Organization.objects.filter(account__account_status='A'),
        widget=forms.HiddenInput,
    )
    details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Event Details")
    start = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), label="Start Date and Time")
    end = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), label="End Date and Time")
    location = forms.CharField(max_length=100, label="Location")
    images = forms.ImageField(label="Event Image", required=False)

    def clean_start(self):
        start_date = self.cleaned_data.get('start')

        if start_date:
            # Ensure start date is not in the past
            if start_date < timezone.now():
                raise forms.ValidationError("Start date cannot be in the past.")

        return start_date

    class Meta:
        model = Event
        fields = ['eventName', 'organizer', 'details', 'start', 'end', 'location', 'images']


class OrganizerFilterForm(forms.Form):
    organizer = forms.ModelChoiceField(queryset=Organization.objects.filter(account__account_status='A'), empty_label="Select Organizer", required=False)
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


class TextPostFilterForm(forms.Form):
    organizer = forms.ModelChoiceField(
                    queryset=Organization.objects.filter(account__account_status='A'),
                    empty_label="Select Organizer",
                    required=False)


class ProfileForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=forms.HiddenInput,
    )
    profile_pic = forms.ImageField(label="Profile Image", required=False)
    details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Description", required=False)
    email = forms.EmailField(max_length=100, required=False)
    contact = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['organization', 'profile_pic', 'details', 'email', 'contact']


class TextPostForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(account__account_status='A'),
        widget=forms.HiddenInput,
    )

    class Meta:
        model = TextPost
        fields = ['organization', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': "What's new?", 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(TextPostForm, self).__init__(*args, **kwargs)
        # Set the maxlength attribute for the 'content' field
        self.fields['content'].widget.attrs['maxlength'] = 500
