import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip_address_management_system.settings')
django.setup()

from ipManager.models import IPAddress

# Define the start and end IP addresses
start_ip = '192.168.1.1'
end_ip = '192.168.1.10'

# Loop through the IP range and insert into the database
for ip_int in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1):
    ip_str = f'192.168.1.{ip_int}'
    status = 'available'  # Set the initial status as 'available'

    # Insert the IP into the database
    IPAddress.objects.create(ip_address=ip_str, status=status)

print("IPs inserted successfully!")

