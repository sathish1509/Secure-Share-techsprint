"""
Script to add YouTube videos to existing courses
"""
import os
import sys
import django
import random
import requests

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

# Now we can import Django models
from courses.models import Course, CourseVideo
from django.conf import settings

def get_youtube_videos(query, max_results=6):
    """Search for videos on YouTube using the API"""
    api_key = settings.YOUTUBE_API_KEY
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part': 'snippet',
        'q': query,
        'maxResults': max_results,
        'key': api_key,
        'type': 'video',
        'videoEmbeddable': 'true',
        'relevanceLanguage': 'en',
        'videoDuration': 'medium',  # Medium length videos (4-20 mins)
    }
    
    try:
        print(f"Searching for videos with query: {query}")
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        # Extract video information
        videos = []
        for item in data.get('items', []):
            video_id = item.get('id', {}).get('videoId')
            if video_id:
                snippet = item.get('snippet', {})
                videos.append({
                    'id': video_id,
                    'title': snippet.get('title', 'Untitled Video'),
                    'description': snippet.get('description', ''),
                })
        
        print(f"Found {len(videos)} videos for query: '{query}'")
        return videos
        
    except Exception as e:
        print(f"YouTube API error: {str(e)}. Using fallback video data.")
        return get_fallback_videos()

def get_fallback_videos():
    """Return fallback video data if YouTube API fails"""
    print("Using fallback video data")
    return [
        {'id': 'rfscVS0vtbw', 'title': 'Learn Python - Full Course for Beginners', 'description': 'Learn Python programming with this comprehensive course'},
        {'id': '_uQrJ0TkZlc', 'title': 'Python Tutorial - Python Full Course for Beginners', 'description': 'Complete Python tutorial for beginners'},
        {'id': 'Z1Yd7upQsXY', 'title': 'Python Tutorial for Absolute Beginners', 'description': 'Step-by-step guide to Python programming'},
        {'id': 'qz0aGYrrlhU', 'title': 'HTML Tutorial for Beginners', 'description': 'Learn HTML from scratch with this tutorial'},
        {'id': 'W6NZfCO5SIk', 'title': 'JavaScript Tutorial for Beginners', 'description': 'Start learning JavaScript programming'}
    ]

def generate_search_query(course):
    """Generate a relevant search query for YouTube based on the course information"""
    # Extract main topic from course title
    title_words = course.title.split()
    # Remove common words
    common_words = ['course', 'introduction', 'fundamentals', 'advanced', 'intermediate', 'to', 'and', 'the', 'for']
    topic_words = [word for word in title_words if word.lower() not in common_words]
    
    # Fallback if no meaningful words found
    if not topic_words:
        topic_words = ['programming', 'tutorial']
        
    # Add difficulty level and educational terms
    query_parts = topic_words[:2]  # Use at most 2 topic words to keep query focused
    query_parts.append(course.difficulty_level)
    query_parts.append('tutorial')
    
    return ' '.join(query_parts)

def add_videos_to_course(course, num_videos=4):
    """Add videos to a course"""
    print(f"Adding videos to course: {course.title} ({course.code})")
    
    # Delete any existing videos
    existing_videos = CourseVideo.objects.filter(course=course)
    if existing_videos.exists():
        print(f"Deleting {existing_videos.count()} existing videos")
        existing_videos.delete()
    
    # Get videos from YouTube API based on course title/topic
    search_query = generate_search_query(course)
    videos = get_youtube_videos(search_query, max_results=num_videos)
    
    # Generic lesson titles
    lesson_titles = [
        'Introduction and Course Overview', 
        'Getting Started with the Basics', 
        'Understanding Core Concepts',
        'Building Your First Project',
        'Advanced Techniques',
        'Practical Applications'
    ]
    
    # Add videos to course
    for i, video_data in enumerate(videos):
        try:
            lesson_title = lesson_titles[i] if i < len(lesson_titles) else f'Lesson {i+1}'
            video = CourseVideo(
                course=course,
                title=f"{lesson_title} - {video_data['title'][:100]}",  # Truncate long titles
                description=video_data.get('description', '')[:500],  # Truncate long descriptions
                youtube_video_id=video_data['id'],
                order=i+1
            )
            video.save()
            print(f"  Added video: {video.title}")
        except Exception as e:
            print(f"  Error adding video: {str(e)}")
            continue
    
    print(f"Added {len(videos)} videos to course {course.code}")
    return len(videos)

def main():
    print("Starting to add videos to courses...")
    
    # Get all courses
    courses = Course.objects.all()
    print(f"Found {courses.count()} courses")
    
    total_videos = 0
    for course in courses:
        videos_added = add_videos_to_course(course)
        total_videos += videos_added
    
    print(f"Successfully added {total_videos} videos to {courses.count()} courses")

if __name__ == "__main__":
    main()
