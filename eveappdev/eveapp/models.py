from django.db import models
#
# # Create your models here.
#


class Account(models.Model):
    accountID = models.BigAutoField(primary_key=True)
    nameApplicant = models.CharField(max_length=150)
    orgName = models.ForeignKey('CreateAccount.Organization', on_delete=models.CASCADE)
    email = models.CharField(max_length=250)
    account_status = models.CharField(max_length=1, choices=(("A", "Approved"), ("R", "Rejected")))

    def __str__(self):
        return f"{self.orgName} {self.account_status}"

    class Meta:
        db_table = "Account"

