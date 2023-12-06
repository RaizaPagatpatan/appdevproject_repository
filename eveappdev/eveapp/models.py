from django.db import models
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

    def __str__(self):
        return self.eventName

    def delete_event(self):
        self.delete()

    class Meta:
        db_table = "Event"

