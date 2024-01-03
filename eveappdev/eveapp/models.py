from django.db import models
from CreateAccount.models import Organization, Student, User
from django.db.models.signals import post_save
from django.utils import timezone


#
# # Create your models here.
#


class Account(models.Model):
    accountID = models.BigAutoField(primary_key=True)
    nameApplicant = models.CharField(max_length=150)
    orgName = models.ForeignKey('CreateAccount.Organization', on_delete=models.CASCADE)
    email = models.CharField(max_length=250)
    details = models.CharField(max_length=250, null=True, blank=True)
    account_status = models.CharField(max_length=1, choices=(("P", "Pending"), ("A", "Approved"), ("R", "Rejected")))
    upload_file = models.FileField(upload_to='verification_files/', null=True, blank=True)


    def __str__(self):
        return f"{self.orgName} {self.account_status}"

    class Meta:
        db_table = "Account"


class Event(models.Model):
    eventID = models.BigAutoField(primary_key=True)
    eventName = models.CharField(max_length=100, verbose_name="Event Name")
    organizer = models.ForeignKey('CreateAccount.Organization', on_delete=models.CASCADE)
    details = models.TextField(verbose_name="Event Details")
    start = models.DateTimeField(verbose_name="Start Date and Time")
    end = models.DateTimeField(verbose_name="End Date and Time")
    location = models.CharField(max_length=100, verbose_name="Location")
    images = models.ImageField(upload_to='event_images/', null=True, blank=True, verbose_name="Event Images")

    rsvp_yes = models.ManyToManyField(Student, through='RSVP', related_name='event_rsvp_yes', blank=True)
    rsvp_no = models.ManyToManyField(Student, related_name='event_rsvp_no', blank=True)

    def __str__(self):
        return self.eventName

    def delete_event(self):
        self.delete()

    class Meta:
        db_table = "Event"


class RSVP(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')  # Ensures a student can only RSVP once to an event


class Profile(models.Model):
    profileID = models.BigAutoField(primary_key=True)
    profile_pic = models.ImageField(upload_to='org_profiles/', null=True, blank=True, verbose_name="Profile Image")
    details = models.TextField(verbose_name="Description")
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=100)

    organization = models.OneToOneField('CreateAccount.Organization', on_delete=models.CASCADE)
    class Meta:
        db_table = "Profile"


#create profile when new org creates account
def create_profile(sender, instance, created, **kwargs):
    if created:
        org_profile = Profile(organization=instance)
        org_profile.save()


post_save.connect(create_profile, sender=Organization)


class Follow(models.Model):
    follower = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='following')
    organization = models.ForeignKey('CreateAccount.Organization', on_delete=models.CASCADE, related_name='followers')

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'organization')
        db_table = "Follow"


class OrgNotification(models.Model):
    org_user = models.ForeignKey('CreateAccount.Organization', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        db_table = "org_notifications"

    def __str__(self):
        return f'{self.org_user.username}: {self.message}'

class StudentNotification(models.Model):
    student_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    event_n = models.ForeignKey('Event', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey('TextPost', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        db_table = "student_notifications"

    def __str__(self):
        return f'{self.student_user.username}: {self.message}'

class Bookmark(models.Model):
    student_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookmarks"

    def __str__(self):
        return f'{self.student_user.username} bookmarked {self.event.title}'


class TextPost(models.Model):
    organization = models.ForeignKey('CreateAccount.Organization', on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Text Content")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "textposts"
        ordering = ['-created_at']

    def __str__(self):
        return f'Text Post by {self.organization.username} at {self.created_at}'

    def delete_textpost(self):
        self.delete()


