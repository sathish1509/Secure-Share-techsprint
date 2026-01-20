from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .forms import CustomUserCreationForm, CustomUserChangeForm, NotificationPreferenceForm
from courses.models import Enrollment
from .coursera_api import get_coursera_courses, get_coursera_access_token

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notification_preference')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def notification_preference(request):
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NotificationPreferenceForm(instance=request.user)
    return render(request, 'accounts/notification_preference.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-date_enrolled')
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'enrollments': enrollments
    })

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(
        student=request.user,
        status='enrolled'
    ).select_related('course')
    return render(request, 'accounts/dashboard.html', {'enrollments': enrollments})

@login_required
def test_coursera_api(request):
    """
    Test view to check the Coursera API integration.
    Only accessible to staff users.
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    # Test getting an access token
    token_data = get_coursera_access_token()
    if not token_data or 'access_token' not in token_data:
        return JsonResponse(
            {'error': 'Failed to get access token from Coursera API'}, 
            status=500
        )
    
    # Test getting courses
    courses = get_coursera_courses(token_data['access_token'])
    if not courses:
        return JsonResponse(
            {'error': 'Failed to get courses from Coursera API'},
            status=500
        )
    
    return JsonResponse({
        'access_token': f"{token_data['access_token'][:10]}... (truncated)",
        'token_type': token_data.get('token_type', 'N/A'),
        'expires_in': token_data.get('expires_in', 'N/A'),
        'courses_count': len(courses.get('elements', [])),
        'sample_courses': [
            {
                'id': course.get('id'),
                'name': course.get('name'),
                'slug': course.get('slug')
            } 
            for course in courses.get('elements', [])[:5]  # Show first 5 courses as sample
        ]
    })
