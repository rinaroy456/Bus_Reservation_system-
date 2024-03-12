
from telnetlib import LOGOUT
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from bookTicket.models import bookAticket
from bus.models import BusInfo, BusPickArea, BusDropArea
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request, template_name="registration/register.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username', '')
            pw = postdata.get('password1', '')
            from django.contrib.auth import authenticate, login
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = reverse('account:my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    
    page_title = 'Registration'
    return render(request, template_name, locals())
import uuid

@login_required
def my_account(request, template_name="registration/my_account.html"):
    page_title = 'My Account'
    uid = uuid.uuid4()

    url ="https://uat.esewa.com.np/epay/transrec"
    q = request.GET.get('ticket_id')
    d = {
        'amt': request.GET.get('amt'),
        'scd': 'EPAYTEST',
        'rid': request.GET.get('refId'),
        'pid': request.GET.get('oid'),
    }
    resp = requests.post(url, d)
    print("status = ",resp.status_code )
    if resp.status_code == 200:
        # Get the transaction ID (pid) from the request
        transaction_id = request.GET.get('oid')
        # Update the status of the specific ticket
        try:
            ticket = bookAticket.objects.get(id=q, user=request.user)
            ticket.status = bookAticket.CONFIRMED
            ticket.save()
        except bookAticket.DoesNotExist:
            # Handle the case where the ticket with the provided transaction ID does not exist
            pass
    tickets = bookAticket.objects.filter(user=request.user)
    for ticket in tickets:
        if ticket.status == bookAticket.CONFIRMED:
            ticket.payment_complete = True
    return render(request, template_name, locals())

import requests
@login_required
def ticket_details(request, ticket_id, template_name="registration/ticketdetails.html"):
    page_title = 'Ticket details'
    tickets = get_object_or_404(bookAticket, id=ticket_id)
    bus_info = get_object_or_404(BusInfo, id=tickets.bus_id)
    bus_arrive = get_object_or_404(BusDropArea, id=bus_info.depature_at_id)
    bus_depart = get_object_or_404(BusPickArea, id=bus_info.arriving_from_id)
    name = request.user.username
    return render(request, template_name, locals())

from django.views.decorators.http import require_POST, require_GET

@require_POST
def logout_view(request):
    LOGOUT(request)
    return redirect('login')


@require_GET
def logout_get(request):
    # Handle GET request for logout (optional)
    return redirect('login')
