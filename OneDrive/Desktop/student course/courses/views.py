from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Course, Enrollment, Announcement, Attendance, CourseVideo
from .forms import CourseForm, AnnouncementForm, CourseVideoForm
from django.db import IntegrityError
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from .utils import search_youtube_videos

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def course_list(request):
    # Prefetch related videos along with enrollments for performance
    courses = Course.objects.all().prefetch_related('enrollment_set', 'videos')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by difficulty level
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        courses = courses.filter(difficulty_level__iexact=difficulty)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        now = timezone.now().date()
        if status == 'upcoming':
            courses = courses.filter(
                Q(start_date__gt=now) | Q(start_date__isnull=True)
            )
        elif status == 'ongoing':
            courses = courses.filter(
                Q(start_date__lte=now, end_date__gte=now) |
                Q(start_date__isnull=False, end_date__isnull=False)
            )
        elif status == 'completed':
            courses = courses.filter(
                Q(end_date__lt=now) | Q(status='completed')
            )
    
    # Get user enrollments for enrolled status
    user_enrollments = set(
        Enrollment.objects.filter(
            student=request.user,
            status='enrolled'
        ).values_list('course_id', flat=True)
    )
    
    # Add enrollment status to each course
    for course in courses:
        course.is_enrolled = course.id in user_enrollments
    
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'search_query': search_query,
        'selected_difficulty': difficulty,
        'selected_status': status,
    })

@login_required
def course_detail(request, course_id):
    # Use select_related and prefetch_related to optimize database queries
    course = get_object_or_404(Course.objects.prefetch_related('videos'), id=course_id)
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course, status='enrolled').exists()
    announcements = Announcement.objects.filter(course=course).order_by('-created_at')
    
    # Get videos for this course in proper order
    videos = course.videos.all().order_by('order')
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'announcements': announcements,
        'videos': videos  # Add videos to the template context
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    existing_enrollment = Enrollment.objects.filter(
        student=request.user, 
        course=course
    ).first()
    
    if existing_enrollment:
        if existing_enrollment.status == 'dropped':
            # Re-enroll if previously dropped
            existing_enrollment.status = 'enrolled'
            existing_enrollment.save()
            messages.success(request, f'Successfully re-enrolled in {course.title}')
        else:
            messages.info(request, f'You are already enrolled in {course.title}')
    else:
        # Create new enrollment
        try:
            if course.available_slots > 0:
                Enrollment.objects.create(student=request.user, course=course)
                messages.success(request, f'Successfully enrolled in {course.title}')
            else:
                messages.error(request, 'Course is full')
        except Exception as e:
            messages.error(request, f'Error enrolling in course: {str(e)}')
    
    return redirect('course_detail', course_id=course_id)

@login_required
def drop_course(request, course_id):
    enrollment = get_object_or_404(Enrollment, student=request.user, course_id=course_id)
    enrollment.status = 'dropped'
    enrollment.save()
    messages.success(request, f'Successfully dropped {enrollment.course.title}')
    return redirect('course_list')

@user_passes_test(is_admin)
def admin_course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/admin_course_list.html', {'courses': courses})

@user_passes_test(is_admin)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully')
            return redirect('admin_course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Create'})

@user_passes_test(is_admin)
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully')
            return redirect('admin_course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Edit'})

@user_passes_test(is_admin)
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('admin_course_list')

@user_passes_test(is_admin)
def create_announcement(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.course = course
            announcement.save()
            messages.success(request, 'Announcement created successfully')
            return redirect('course_detail', course_id=course_id)
    else:
        form = AnnouncementForm()
    return render(request, 'courses/announcement_form.html', {
        'form': form,
        'course': course
    })

@login_required
def attendance_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_teacher = request.user.is_staff or request.user.is_superuser
    
    if request.method == 'POST' and is_teacher:
        date = request.POST.get('date')
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        attendance, created = Attendance.objects.update_or_create(
            student_id=student_id,
            course=course,
            date=date,
            defaults={
                'status': status,
                'notes': notes,
                'marked_by': request.user
            }
        )
        return JsonResponse({'status': 'success'})
    
    # Get enrolled students
    enrollments = Enrollment.objects.filter(course=course, status='enrolled')
    
    # Get attendance data for the last 30 days
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    attendance_data = Attendance.objects.filter(
        course=course,
        date__gte=thirty_days_ago
    ).values('student', 'date', 'status')
    
    # Calculate attendance statistics
    attendance_stats = Attendance.objects.filter(course=course).values(
        'student'
    ).annotate(
        total_classes=Count('id'),
        present_count=Count('id', filter=Q(status='present')),
        absent_count=Count('id', filter=Q(status='absent')),
        late_count=Count('id', filter=Q(status='late'))
    )
    
    return render(request, 'courses/attendance.html', {
        'course': course,
        'enrollments': enrollments,
        'attendance_data': attendance_data,
        'attendance_stats': attendance_stats,
        'is_teacher': is_teacher,
    })

@login_required
def student_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    attendance = Attendance.objects.filter(
        course=course,
        student=request.user
    ).order_by('-date')
    
    # Calculate statistics
    total_classes = attendance.count()
    present_count = attendance.filter(status='present').count()
    attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
    
    return render(request, 'courses/student_attendance.html', {
        'course': course,
        'attendance': attendance,
        'total_classes': total_classes,
        'present_count': present_count,
        'attendance_percentage': attendance_percentage,
    })

@login_required
def course_videos(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    return render(request, 'courses/course_videos.html', {
        'course': course,
        'videos': videos
    })

@user_passes_test(is_admin)
def add_course_video(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseVideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            messages.success(request, 'Video added successfully')
            return redirect('course_videos', course_id=course.id)
    else:
        form = CourseVideoForm()
    return render(request, 'courses/video_form.html', {
        'form': form,
        'course': course,
        'action': 'Add'
    })

@user_passes_test(is_admin)
def edit_course_video(request, course_id, video_id):
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(CourseVideo, id=video_id, course=course)
    if request.method == 'POST':
        form = CourseVideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully')
            return redirect('course_videos', course_id=course.id)
    else:
        form = CourseVideoForm(instance=video)
    return render(request, 'courses/video_form.html', {
        'form': form,
        'course': course,
        'action': 'Edit'
    })

@user_passes_test(is_admin)
def delete_course_video(request, course_id, video_id):
    video = get_object_or_404(CourseVideo, id=video_id, course_id=course_id)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully')
        return redirect('course_videos', course_id=course_id)
    
    return render(request, 'courses/video_confirm_delete.html', {
        'video': video,
        'course': video.course
    })

@login_required
def view_course_video(request, course_id, video_id):
    # Get the course and video objects or return 404 if not found
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(CourseVideo, id=video_id, course_id=course_id)
    
    # Get the student's enrollment status
    enrollment = None
    is_enrolled = False
    
    if not request.user.is_staff:
        # Check if student is enrolled in this course
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        is_enrolled = enrollment and enrollment.status == 'enrolled'
        
        # If not enrolled and not staff, redirect with message
        if not is_enrolled:
            messages.warning(request, 'You must be enrolled in this course to view its videos.')
            return redirect('course_detail', course_id=course_id)
    
    # Generate the absolute URL for sharing
    video_absolute_url = request.build_absolute_uri()
    
    return render(request, 'courses/view_video.html', {
        'course': course,
        'video': video,
        'is_enrolled': is_enrolled,
        'video_url': video_absolute_url
    })

@user_passes_test(is_admin)
def search_youtube_videos_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = []
    search_query = None
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            # Add course title to search query for better results
            full_query = f"{course.title} {search_query}"
            videos = search_youtube_videos(full_query)
            
            # If videos are found, add them to the course
            if videos and request.POST.get('add_all'):
                for video_data in videos:
                    CourseVideo.objects.create(
                        course=course,
                        title=video_data['title'],
                        description=video_data['description'],
                        youtube_video_id=video_data['youtube_video_id']
                    )
                messages.success(request, f'Added {len(videos)} videos to the course')
                return redirect('course_videos', course_id=course.id)
    
    return render(request, 'courses/search_videos.html', {
        'course': course,
        'videos': videos,
        'search_query': search_query
    })
