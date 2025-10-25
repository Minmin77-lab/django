from django.shortcuts import render, get_object_or_404
from .models import Users, Staff, Attractions, Tickets, TicketTypes

def attractions(request):
    all_attractions = Attractions.objects.select_related('staff').all()
    return render(request, 'attractions.html', {'attractions_list': all_attractions})

def tickets(request):
    all_tickets = Tickets.objects.select_related('user', 'ticket_type').all().order_by('-purchase_date')
    all_ticket_types = TicketTypes.objects.all()
    context = {
        'tickets_list': all_tickets,
        'ticket_types': all_ticket_types,
    }
    return render(request, 'tickets.html', context)

def users(request):
    all_users = Users.objects.all().order_by('surname', 'name') 
    return render(request, 'users.html', {'users_list': all_users})

def staff(request):
    all_staff = Staff.objects.all().order_by('surname', 'name')  
    return render(request, 'staff.html', {'staff_list': all_staff})

def attraction_detail(request, pk):
    attraction_data = get_object_or_404(Attractions, pk=pk)
    return render(request, 'attraction.html', {'attraction': attraction_data})