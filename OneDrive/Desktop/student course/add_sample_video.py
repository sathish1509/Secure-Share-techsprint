import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

# Import models after setting up Django
from courses.models import Course, CourseVideo

def add_sample_videos():
    """Add sample videos to the first course in the database."""
    try:
        # Get the first course
        course = Course.objects.first()
        
        if not course:
            print("No courses found in the database.")
            return
        
        # Check if the course already has videos
        if CourseVideo.objects.filter(course=course).exists():
            print(f"Course '{course.title}' already has videos.")
            return
        
        # Sample videos with YouTube IDs
        sample_videos = [
            {
                'title': 'Introduction to the Course',
                'description': 'Welcome to the course! This video introduces the main topics we will cover.',
                'youtube_video_id': 'dQw4w9WgXcQ',  # Sample YouTube ID
                'order': 1
            },
            {
                'title': 'Key Concepts Overview',
                'description': 'An overview of the key concepts and skills you will learn in this course.',
                'youtube_video_id': '9bZkp7q19f0',  # Sample YouTube ID
                'order': 2
            }
        ]
        
        # Add videos to the course
        videos_added = []
        for video_data in sample_videos:
            video = CourseVideo.objects.create(
                course=course,
                **video_data
            )
            videos_added.append(video.title)
        
        print(f"Added {len(videos_added)} sample videos to '{course.title}':")
        for title in videos_added:
            print(f" - {title}")
            
    except Exception as e:
        print(f"Error adding sample videos: {str(e)}")

if __name__ == "__main__":
    add_sample_videos()
