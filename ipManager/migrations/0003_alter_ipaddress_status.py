# Generated by Django 4.2.5 on 2023-10-05 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipManager', '0002_remove_ipaddress_broadcast_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipaddress',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('allocated', 'Allocated')], max_length=10),
        ),
    ]