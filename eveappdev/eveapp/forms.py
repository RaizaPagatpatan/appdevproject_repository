from django import forms
from .models import Account
from django.apps import apps

Organization = apps.get_model('CreateAccount', 'Organization')
Student = apps.get_model('CreateAccount', 'Student')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


# class OrgVerifyForm(forms.ModelForm):
#     orgName = forms.CharField(max_length=100, label="Organization Name")
#     nameApplicant = forms.ModelChoiceField(
#         queryset=Organization.objects.all(),
#         widget=forms.HiddenInput,
#     )
#     applicantPosition = forms.CharField(max_length=100, label="Position of Apllicant")
#
#     event_status = forms.CharField(widget=forms.HiddenInput, initial='P')
#     document = forms.FileField(label="Upload Requirement")
#
#     class Meta:
#         model = Account
#         fields = ['orgName', 'nameApplicant', 'applicantPosition', 'account_status', 'document']


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
    nameApplicant = forms.CharField(max_length=150, label="Name of Applicant")
    org_Name = forms.CharField(max_length=100, label="Organization Name")
    orgName = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=forms.HiddenInput,
        required=False
    )
    email = forms.EmailField(max_length=250)
    details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Applicant Details")
    account_status = forms.CharField(
        widget=forms.HiddenInput,
        initial='P')
    upload_file = forms.FileField(label="Upload Accreditation Certificate")
    class Meta:
        model = Account
        fields = ['org_Name', 'orgName', 'email', 'details', 'account_status', 'upload_file']
