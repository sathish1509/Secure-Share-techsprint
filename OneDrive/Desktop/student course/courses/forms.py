from django import forms
from .models import Course, Announcement, CourseVideo

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'credits', 'instructor', 'max_students', 'website_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'website_link': forms.URLInput(attrs={'placeholder': 'https://example.com'})
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']

class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ['title', 'description', 'youtube_video_id', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'youtube_video_id': forms.TextInput(attrs={'placeholder': 'Enter YouTube video ID (e.g., dQw4w9WgXcQ)'}),
        } 