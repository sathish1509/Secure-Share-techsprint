from googleapiclient.discovery import build
from django.conf import settings

def search_youtube_videos(query, max_results=10):
    """
    Search YouTube videos based on the given query.
    Returns a list of video information including title, description, and video ID.
    """
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        # Search for videos
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            videoEmbeddable='true',
            relevanceLanguage='en'
        ).execute()

        videos = []
        for item in search_response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_data = {
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                    'youtube_video_id': item['id']['videoId'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_data)
        
        return videos
    except Exception as e:
        print(f"Error searching YouTube videos: {str(e)}")
        return [] 