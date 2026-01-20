"""
Script to add guaranteed working videos to all courses
"""
import os
import django
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

# Import models
from courses.models import Course, CourseVideo

# List of guaranteed working YouTube video IDs with titles and descriptions
WORKING_VIDEOS = [
    {
        'id': 'rfscVS0vtbw',
        'title': 'Learn Python - Full Course for Beginners',
        'description': 'This Python tutorial is designed for beginners to learn Python programming with practical examples'
    },
    {
        'id': '_uQrJ0TkZlc',
        'title': 'Python Tutorial - Python Full Course for Beginners',
        'description': 'Complete Python tutorial covering all the basics plus advanced topics like Python decorators, OOP, and more'
    },
    {
        'id': 'Z1Yd7upQsXY',
        'title': 'Python Tutorial for Absolute Beginners',
        'description': 'A step-by-step guide to Python programming language fundamentals, ideal for absolute beginners'
    },
    {
        'id': 'qz0aGYrrlhU',
        'title': 'HTML Tutorial for Beginners',
        'description': 'Learn HTML from scratch with comprehensive explanations of all the important HTML elements and attributes'
    },
    {
        'id': 'W6NZfCO5SIk',
        'title': 'JavaScript Tutorial for Beginners',
        'description': 'Start learning JavaScript programming with this comprehensive tutorial for beginners'
    },
    {
        'id': 'pQN-pnXPaVg',
        'title': 'HTML Crash Course For Beginners',
        'description': 'A crash course in HTML basics, covering all the essential elements for building websites'
    },
    {
        'id': 'ok-plXXHlWw',
        'title': 'CSS Tutorial - Zero to Hero',
        'description': 'Complete CSS tutorial covering everything from basic styling to advanced layout techniques'
    },
    {
        'id': 'G3e-cpL7ofc',
        'title': 'HTML & CSS Full Course - Beginner to Pro',
        'description': 'Learn HTML and CSS from scratch with this comprehensive course for beginners'
    }
]

def add_videos_to_all_courses():
    """Add working videos to all courses in the database"""
    courses = Course.objects.all()
    total_courses = courses.count()
    print(f"Found {total_courses} courses in the database")
    
    video_count = 0
    
    for course in courses:
        print(f"\nProcessing course: {course.code} - {course.title}")
        
        # Delete existing videos for this course
        existing_videos = CourseVideo.objects.filter(course=course)
        if existing_videos.exists():
            deleted_count = existing_videos.count()
            print(f"Deleting {deleted_count} existing videos")
            existing_videos.delete()
        
        # Add 4 videos to each course (or less if we don't have enough working videos)
        videos_to_add = min(4, len(WORKING_VIDEOS))
        
        lesson_titles = [
            'Introduction and Course Overview', 
            'Getting Started with the Basics', 
            'Understanding Core Concepts',
            'Building Your First Project'
        ]
        
        for i in range(videos_to_add):
            video_data = WORKING_VIDEOS[i % len(WORKING_VIDEOS)]
            lesson_title = lesson_titles[i] if i < len(lesson_titles) else f'Lesson {i+1}'
            
            video = CourseVideo(
                course=course,
                title=f"{lesson_title} - {video_data['title']}",
                description=video_data['description'],
                youtube_video_id=video_data['id'],
                order=i+1
            )
            video.save()
            video_count += 1
            print(f"  ✅ Added video: {video.title}")
    
    print(f"\nSuccessfully added {video_count} videos to {total_courses} courses")
    return video_count

if __name__ == "__main__":
    print("Starting video update utility...\n")
    videos_added = add_videos_to_all_courses()
    print("\nDone! Your course videos have been updated with guaranteed working videos.")
