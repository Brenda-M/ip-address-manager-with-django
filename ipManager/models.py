from django.db import models

# Customer Model: Represents customer information


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.customer_name


class IPAddress(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('allocated', 'Allocated'),
        ('reserved', 'Reserved'),
    )
    ip_address = models.GenericIPAddressField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.ip_address

    class Meta:
        db_table = 'ipmanager_ipaddress'
