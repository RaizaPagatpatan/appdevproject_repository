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

