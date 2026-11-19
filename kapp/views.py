from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Contact, reservation


def index(request):
    if request.method == 'POST':
        raw_time = request.POST.get('time')

        parsed_time = None
        for fmt in ('%I:%M %p', '%H:%M'):
            try:
                parsed_time = datetime.strptime(raw_time, fmt).time()
                break
            except (ValueError, TypeError):
                continue

        if parsed_time is None:
            messages.error(request, 'Please choose a valid time.')
            return redirect('index')

        reservation.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            date=request.POST.get('date'),
            time=parsed_time,                      # use the parsed value
            number_of_guests=request.POST.get('number_of_guests'),
            special_requests=request.POST.get('special_requests'),

        )
        messages.success(request, 'Reservation made successfully!')
        return redirect('index')                   # avoids duplicate submits on refresh

    return render(request, 'index.html')

def contact(request):
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        subject = (request.POST.get('subject') or '').strip()
        phone_number = (request.POST.get('phone_number') or '').strip()
        message = (request.POST.get('message') or '').strip()

        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('/#contact-section')

        contact_entry = Contact(
            name=name,
            email=email,
            subject=subject,
            phone_number=phone_number,
            message=message
        )
        contact_entry.save()

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('index')

    return render(request, 'index.html')