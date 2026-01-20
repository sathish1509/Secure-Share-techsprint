from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ]

    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.IntegerField()
    instructor = models.CharField(max_length=100)
    max_students = models.IntegerField()
    website_link = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    prerequisites = models.TextField(blank=True, null=True)
    syllabus = models.TextField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, 
                               validators=[MinValueValidator(0.00), MaxValueValidator(5.00)])
    total_ratings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.code} - {self.title}"

    @property
    def available_slots(self):
        return self.max_students - self.enrollment_set.count()
        
    @property
    def progress_percentage(self):
        # Handle completed and upcoming statuses first
        if self.status == 'completed':
            return 100
        elif self.status == 'upcoming':
            return 0
            
        # Check if we have both dates before calculating
        if not self.start_date or not self.end_date:
            return 0
            
        # Calculate progress based on start and end dates
        from django.utils import timezone
        import datetime
        today = timezone.now().date()
        
        # Calculate total days in course
        total_days = (self.end_date - self.start_date).days
        if total_days <= 0:  # Handle case where end_date <= start_date
            return 0
            
        # Calculate days passed
        days_passed = (today - self.start_date).days
        if days_passed < 0:
            return 0
            
        # Calculate progress percentage
        progress = min(100, int((days_passed / total_days) * 100))
        return progress

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed')
    ], default='enrolled')

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} - {self.course.code}"

class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']
        
    def save(self, *args, **kwargs):
        # Update course rating on save
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Recalculate course rating
        course = self.course
        avg_rating = CourseReview.objects.filter(course=course).aggregate(
            models.Avg('rating'))['rating__avg']
        course.rating = round(avg_rating, 2) if avg_rating else 0.00
        course.total_ratings = CourseReview.objects.filter(course=course).count()
        course.save()

class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ])
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='marked_attendances'
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} - {self.course.code} - {self.date}"

class CourseVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    youtube_video_id = models.CharField(max_length=20, help_text="YouTube video ID (e.g., dQw4w9WgXcQ)")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'youtube_video_id']

    def __str__(self):
        return f"{self.course.code} - {self.title}"

    @property
    def youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_video_id}"

    @property
    def youtube_thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_video_id}/mqdefault.jpg"
