from django.db import models

# Create your models here.



class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, default=user_id)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    type = (("S", "Student"), ("O", "Organization"), ("A", "Admin"))
    user_type = models.CharField(max_length=1, choices=type)

    class Meta:
        abstract = True


class Student(User):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "Student"


class Organization(User):
    organization_name = models.CharField(max_length=100)
    # name_orgUser = models.CharField(max_length=100)


    def __str__(self):
        return self.organization_name

    class Meta:
        db_table = "Organization"


class Admin(User):
    admin_status = models.CharField(max_length=1, choices=(("A", "Active"), ("I", "Inactive")))
    approve_Account = models.OneToOneField("eveapp.Account", on_delete=models.CASCADE)

    def __str__(self):
        return "admin"

    class Meta:
        db_table = "Admin"