from django.db import models


# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=100, blank=False)
    contact_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=100, blank=True)
    

class Inventory(models.Model):
    class ColorType(models.TextChoices):
        BLUE = 'Blue'
        GREY = 'Grey'
        BLACK = 'Black'
        WHITE = 'White'
        PURPLE = 'Purple'
    color = models.CharField(max_length=16, choices=ColorType.choices, default=None)
    quantity = models.PositiveIntegerField(blank=False, default=0)
    class StatusType(models.TextChoices):
        AVAILABLE = 'Available'
        LOW = 'Low'
        EMPTY = 'Empty'
    status = models.CharField(max_length=16, choices=StatusType.choices, default=StatusType.EMPTY)
    last_updated = models.DateTimeField(auto_now=True, blank=False)


class Role(models.Model):
    class RoleType(models.TextChoices):
        MANAGER = 'Manager',
        ADMIN = 'Admin',
        PAINTER = 'Painter'
    role = models.CharField(max_length=16, choices=RoleType.choices, default=None)

    def __str__(self):
        return f"{self.role}"
    

class Permission(models.Model):
    class PermissionType(models.TextChoices):
        VIEW = 'View',
        UPDATE = 'Update',
        ADMIN = 'Admin'
    permission = models.CharField(max_length=16, choices=PermissionType.choices, default=None)

    def __str__(self):
        return f"{self.permission}"
    

class Employee(models.Model):
    name = models.CharField(max_length=100, blank=False)
    age = models.PositiveIntegerField(max_length=80, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=100, blank=True)
    role = models.ManyToManyField(Role)
    permission = models.ManyToManyField(Permission)

    def __str__(self):
        return f"{self.name}"
    

class Property(models.Model):
    class PropertyType(models.TextChoices):
        HOUSES = 'Houses'
    property_type = models.CharField(max_length=16, choices=PropertyType.choices, default=PropertyType.HOUSES)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.property_type}"
    

class PropertyAssignment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    class Status(models.TextChoices):
        ACTIVE = 'Active',
        INACTIVE = 'Inactive',
    status = models.CharField(max_length=16, choices=Status.choices, default=None)