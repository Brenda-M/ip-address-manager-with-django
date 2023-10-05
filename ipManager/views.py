from .models import IPAddress, Customer
from django.http import JsonResponse
from rest_framework import status
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Customer, IPAddress
from django.shortcuts import render, get_object_or_404, redirect
from ipaddress import IPv4Interface
from .forms import SubnetCalculatorForm
import json


def home(request):
    ip_addresses = IPAddress.objects.all()
    customers = Customer.objects.all()
    context = {
        'ip_addresses': ip_addresses,
        'customers': customers,
    }
    return render(request, 'main.html', context)


def list_available_ips(request):
    available_ips = IPAddress.objects.filter(status='available')
    return render(request, 'list_available_ips.html', {'available_ips': available_ips})


def list_allocated_ips(request):
    allocated_ips = IPAddress.objects.filter(status='allocated')
    return render(request, 'allocated_ips.html', {'allocated_ips': allocated_ips})


def release_ip_address(request, ip_address):
    try:
        # Attempt to get the IPAddress object by its IP address
        ip_obj = get_object_or_404(IPAddress, ip_address=ip_address)

        if ip_obj.status == 'allocated':
            # Release the IP address by changing its status
            ip_obj.status = 'available'
            ip_obj.customer = None
            ip_obj.save()

            messages.success(request, 'IP address released successfully')
        else:
            messages.error(
                request, 'IP address is not allocated and cannot be released')

        return redirect('/')

    except IPAddress.DoesNotExist:
        messages.error(request, 'IP address not found')

        return redirect('/')


def unreserve_ip_address(request, ip_address):
    try:
        ip = IPAddress.objects.get(ip_address=ip_address)
        if ip.status == 'reserved':
            ip.status = 'available'
            ip.save()
    except IPAddress.DoesNotExist:
        pass  # Handle the case where the IP address doesn't exist
    # Redirect to the list of available IPs or a suitable page
    return HttpResponseRedirect(reverse('home'))


def allocate_ip_address(request):
    if request.method == 'POST':
        try:
            # Get the selected allocation type (existing or new customer)
            allocation_type = request.POST.get('allocation_type')
            print(allocation_type)

            # Check if allocation_type is not specified or invalid
            if allocation_type not in ['existing', 'new']:
                messages.error(request, 'Invalid allocation type')
                return redirect('/')

            # Handle allocation to an existing customer
            if allocation_type == 'existing':
                # Get the selected customer's ID from the form submission
                selected_customer_id = request.POST.get('selected_customer_id')

                # Check if there are available IP addresses
                available_ip = IPAddress.objects.filter(
                    status='available').first()

                if available_ip:
                    # Check if the IP is already allocated
                    if available_ip.status == 'allocated':
                        messages.error(request, 'IP address already allocated')
                        return redirect('your_redirect_view_name')

                    # Allocate the available IP address to the customer
                    available_ip.status = 'allocated'
                    available_ip.customer = Customer.objects.get(
                        pk=selected_customer_id)
                    available_ip.save()

                    # Add a success message
                    messages.success(
                        request, 'IP address allocated successfully')
                else:
                    # Add an error message
                    messages.error(request, 'No available IP addresses')

            # Handle allocation to a new customer
            elif allocation_type == 'new':
                # Extract new customer information from the form
                new_customer_name = request.POST.get('new_customer_name')
                new_customer_email = request.POST.get('new_customer_email')

                # Create a new customer
                customer, created = Customer.objects.get_or_create(
                    customer_name=new_customer_name,
                    email=new_customer_email,
                )

                if not created:
                    messages.error(
                        request, 'Customer with this email already exists')
                    return redirect('/')

                # Check if there are available IP addresses
                available_ip = IPAddress.objects.filter(
                    status='available').first()

                if available_ip:
                    # Check if the IP is already allocated
                    if available_ip.status == 'allocated':
                        messages.error(request, 'IP address already allocated')
                        return redirect('/')

                    # Allocate the available IP address to the new customer
                    available_ip.status = 'allocated'
                    available_ip.customer = customer
                    available_ip.save()

                    # Add a success message
                    messages.success(
                        request, 'IP address allocated successfully')
                else:
                    # Add an error message
                    messages.error(request, 'No available IP addresses')

            # Redirect to an appropriate view
            return redirect('/')

        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found')
        except Exception as e:
            # Add an error message with the exception details
            messages.error(request, f'An error occurred: {str(e)}')

        # Redirect to an appropriate view
        return redirect('/')


def subnet_calculator(request):
    result = None

    if request.method == 'POST':
        form = SubnetCalculatorForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data['ip_address']
            network_class = form.cleaned_data['network_class']
            subnet_mask_cidr = form.cleaned_data['subnet_mask']

            # Check if a specific subnet mask is provided by the user
            if subnet_mask_cidr:
                network = IPv4Interface(f"{ip_address}/{subnet_mask_cidr}")
            else:
                # Determine the subnet mask based on the network class
                subnet_mask_cidr_from_class = {
                    'A': '8',
                    'B': '16',
                    'C': '24',
                }.get(network_class)

                if subnet_mask_cidr_from_class is not None:
                    network = IPv4Interface(
                        f"{ip_address}/{subnet_mask_cidr_from_class}")
                else:
                    # Invalid network class provided
                    network = None

            if network:
                result = {
                    'network_address': network.network.network_address,
                    'broadcast_address': network.network.broadcast_address,
                }

                # Check if there are usable IP addresses
                if network.network.network_address + 1 < network.network.broadcast_address:
                    result['usable_ip_range'] = f"{network.network.network_address + 1} - {network.network.broadcast_address - 1}"
                else:
                    result['usable_ip_range'] = 'None'
    else:
        form = SubnetCalculatorForm()

    return render(request, 'subnet_calculator.html', {'form': form, 'result': result})


def filter_ips_by_range(request):
    try:
        # Get the start and end IP addresses from the request's query parameters
        start_ip = request.GET.get('start_ip')
        end_ip = request.GET.get('end_ip')

        if not start_ip or not end_ip:
            return JsonResponse({'message': 'Both start_ip and end_ip parameters are required.'}, status=400)

        filtered_ips = IPAddress.objects.filter(
            status='available',
            ip_address__gte=start_ip,
            ip_address__lte=end_ip
        )

        ip_list = [{'ip_address': ip.ip_address, 'status': ip.status}
                   for ip in filtered_ips]

        return JsonResponse({'filtered_ips': ip_list}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Bad request'}, status=400)

