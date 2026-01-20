import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

# Import models after setting up Django
from courses.models import Course, CourseVideo

def add_videos_to_all_courses():
    """Add sample videos to ALL courses in the database."""
    try:
        # Get all courses
        courses = Course.objects.all()
        
        if not courses:
            print("No courses found in the database.")
            return
        
        total_videos_added = 0
        
        # Sample videos with YouTube IDs (popular educational content)
        sample_videos = [
            {
                'title': 'Introduction to Computer Science',
                'description': 'This video introduces the fundamentals of computer science and programming.',
                'youtube_video_id': 'zOjov-2OZ0E',  # MIT OpenCourseWare video
                'order': 1
            },
            {
                'title': 'Machine Learning Basics',
                'description': 'Learn the basic concepts of machine learning and AI.',
                'youtube_video_id': 'aircAruvnKk',  # 3Blue1Brown video
                'order': 2
            },
            {
                'title': 'Web Development Crash Course',
                'description': 'A quick overview of modern web development technologies.',
                'youtube_video_id': 'gQojMIhELvM',  # Web dev tutorial
                'order': 3
            }
        ]
        
        # Process each course
        for course in courses:
            print(f"Processing course: {course.title}")
            
            # Delete any existing videos first
            existing_count = CourseVideo.objects.filter(course=course).count()
            if existing_count > 0:
                print(f"  - Removing {existing_count} existing videos")
                CourseVideo.objects.filter(course=course).delete()
            
            # Add videos to the course
            videos_added = []
            for video_data in sample_videos:
                video = CourseVideo.objects.create(
                    course=course,
                    **video_data
                )
                videos_added.append(video.title)
                total_videos_added += 1
            
            print(f"  - Added {len(videos_added)} videos to '{course.title}'")
            
        print(f"\nTotal: Added {total_videos_added} videos across {courses.count()} courses")
        print("Video functionality is now ready to use!")
            
    except Exception as e:
        print(f"Error adding videos: {str(e)}")
        # Print more detailed error information
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Adding videos to all courses...")
    add_videos_to_all_courses()
    print("\nDone! You can now view videos in your courses.")
