from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Users, Staff, Attractions, Tickets, TicketTypes, SearchHistory

def save_search_history(query, search_type, user):
    if query.strip():
        SearchHistory.objects.create(
            query=query,
            search_type=search_type,
            user=user if user.is_authenticated else None
        )

def get_recent_searches(user, search_type, limit=5):
    if user.is_authenticated:
        recent = SearchHistory.objects.filter(
            user=user,
            search_type=search_type
        ).values_list('query', flat=True).distinct()[:limit]
    else:
        recent = SearchHistory.objects.filter(
            search_type=search_type
        ).values_list('query', flat=True).distinct()[:limit]
    return list(recent)

def attractions(request):
    query = request.GET.get('query', '').strip()
    all_attractions = Attractions.objects.select_related('staff').all()
    
    if query:
        save_search_history(query, 'attractions', request.user)
        all_attractions = all_attractions.filter(
            Q(name__icontains=query) |
            Q(staff__name__icontains=query) |
            Q(staff__surname__icontains=query)
        )
    
    recent_searches = get_recent_searches(request.user, 'attractions')
    
    return render(request, 'attractions.html', {
        'attractions_list': all_attractions,
        'search_query': query,
        'recent_searches': recent_searches
    })

def tickets(request):
    query = request.GET.get('query', '').strip()
    selected_types = request.GET.getlist('type')
    
    all_tickets = Tickets.objects.select_related('user', 'ticket_type').all().order_by('-purchase_date')
    all_ticket_types = TicketTypes.objects.all()
    
    if selected_types:
        all_tickets = all_tickets.filter(ticket_type__name__in=selected_types)
    
    if query:
        save_search_history(query, 'tickets', request.user)
        all_tickets = all_tickets.filter(
            Q(user__name__icontains=query) |
            Q(user__surname__icontains=query) |
            Q(ticket_type__name__icontains=query) |
            Q(id__icontains=query)
        )
    
    recent_searches = get_recent_searches(request.user, 'tickets')
    
    context = {
        'tickets_list': all_tickets,
        'ticket_types': all_ticket_types,
        'selected_types': selected_types,
        'search_query': query,
        'recent_searches': recent_searches
    }
    
    return render(request, 'tickets.html', context)

def users(request):
    query = request.GET.get('query', '').strip()
    all_users = Users.objects.all().order_by('surname', 'name')
    
    if query:
        save_search_history(query, 'users', request.user)
        all_users = all_users.filter(
            Q(name__icontains=query) |
            Q(surname__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
    
    recent_searches = get_recent_searches(request.user, 'users')
    
    return render(request, 'users.html', {
        'users_list': all_users,
        'search_query': query,
        'recent_searches': recent_searches
    })

def staff(request):
    query = request.GET.get('query', '').strip()
    all_staff = Staff.objects.all().order_by('surname', 'name')
    
    if query:
        save_search_history(query, 'staff', request.user)
        all_staff = all_staff.filter(
            Q(name__icontains=query) |
            Q(surname__icontains=query) |
            Q(position__icontains=query) |
            Q(phone_number__icontains=query)
        )
    
    recent_searches = get_recent_searches(request.user, 'staff')
    
    return render(request, 'staff.html', {
        'staff_list': all_staff,
        'search_query': query,
        'recent_searches': recent_searches
    })

def attraction_detail(request, pk):
    attraction_data = get_object_or_404(Attractions, pk=pk)
    return render(request, 'attraction.html', {'attraction': attraction_data})