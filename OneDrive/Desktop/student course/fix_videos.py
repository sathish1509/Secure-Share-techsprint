"""
Script to fix and refresh YouTube videos for existing courses
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

def verify_youtube_api():
    """Verify the YouTube API key is working"""
    api_key = settings.YOUTUBE_API_KEY
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part': 'snippet',
        'q': 'test',
        'maxResults': 1,
        'key': api_key,
        'type': 'video',
    }
    
    try:
        print(f"Testing YouTube API key...")
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            print("✅ YouTube API key is working!")
            return True
        else:
            print("❌ YouTube API key is not returning any results")
            return False
            
    except Exception as e:
        print(f"❌ YouTube API error: {str(e)}")
        return False

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
        {'id': 'W6NZfCO5SIk', 'title': 'JavaScript Tutorial for Beginners', 'description': 'Start learning JavaScript programming'},
        {'id': 'pQN-pnXPaVg', 'title': 'HTML Tutorial for Beginners: HTML Crash Course', 'description': 'A crash course in HTML for beginners'},
        {'id': 'ok-plXXHlWw', 'title': 'CSS Tutorial - Zero to Hero', 'description': 'Complete CSS tutorial for beginners'},
        {'id': 'G3e-cpL7ofc', 'title': 'HTML & CSS Full Course - Beginner to Pro', 'description': 'Learn HTML and CSS from scratch'},
        {'id': 'f5TupRFKW64', 'title': 'Build and Deploy a Personal Portfolio with React', 'description': 'Build a modern portfolio with React.js'},
        {'id': 'jc1phpnWHqY', 'title': 'Django for Beginners - Full Tutorial', 'description': 'Django tutorial for beginners'}
    ]

def verify_and_fix_videos():
    """Verify all course videos are valid and fix any issues"""
    print("\nVerifying and fixing course videos...")
    
    # Get all videos
    videos = CourseVideo.objects.all()
    print(f"Found {videos.count()} videos in database")
    
    # Fallback videos
    fallback_videos = get_fallback_videos()
    fallback_index = 0
    
    # Verify each video
    fixed_count = 0
    for video in videos:
        print(f"\nChecking video: {video.title}")
        
        try:
            # Check if the video ID is valid
            url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video.youtube_video_id}&format=json"
            response = requests.head(url)
            
            if response.status_code == 200:
                print(f"✅ Video ID {video.youtube_video_id} is valid")
                continue
            else:
                print(f"❌ Video ID {video.youtube_video_id} is invalid or unavailable")
                
                # Replace with fallback video
                fallback = fallback_videos[fallback_index % len(fallback_videos)]
                fallback_index += 1
                
                video.youtube_video_id = fallback['id']
                video.save()
                print(f"  ✓ Fixed with fallback video ID: {fallback['id']}")
                fixed_count += 1
                
        except Exception as e:
            print(f"  Error checking video: {str(e)}")
            
            # Replace with fallback video
            fallback = fallback_videos[fallback_index % len(fallback_videos)]
            fallback_index += 1
            
            video.youtube_video_id = fallback['id']
            video.save()
            print(f"  ✓ Fixed with fallback video ID: {fallback['id']}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} videos")
    return fixed_count

def main():
    print("Starting video fix utility...")
    
    # First verify YouTube API
    api_working = verify_youtube_api()
    
    # Then verify and fix videos
    fixed_count = verify_and_fix_videos()
    
    print(f"\nSummary:")
    print(f"YouTube API working: {'Yes' if api_working else 'No'}")
    print(f"Fixed videos: {fixed_count}")
    print("Done!")

if __name__ == "__main__":
    main()
