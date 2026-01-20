from django.core.management.base import BaseCommand
from django.conf import settings
from courses.models import Course, CourseVideo
import logging
from datetime import datetime, timedelta
import requests
import random
import json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch courses from public APIs and update database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching courses from public APIs...')
        
        # First, clear existing courses and videos
        CourseVideo.objects.all().delete()
        Course.objects.all().delete()
        self.stdout.write('Existing courses and videos cleared')
        
        # Fetch courses from multiple sources
        total_courses = 0
        
        # Try to fetch from Open University API (no auth required)
        self.stdout.write('Fetching courses from Open University API...')
        ou_courses = self.fetch_open_university_courses()
        if ou_courses:
            total_courses += len(ou_courses)
        
        # Fetch udacity courses (using their public catalog, no auth required)
        self.stdout.write('Fetching courses from Udacity API...')
        udacity_courses = self.fetch_udacity_courses()
        if udacity_courses:
            total_courses += len(udacity_courses)
            
        # If we still don't have many courses, add some mock data
        if total_courses < 20:
            self.stdout.write('Adding mock courses to database...')
            mock_courses = self.create_mock_courses(20 - total_courses)
            total_courses += len(mock_courses)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched {total_courses} courses'))

    def fetch_open_university_courses(self):
        """Fetch courses from Open University's public API"""
        api_url = "http://data.open.ac.uk/query?query=PREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+mlo%3A+%3Chttp%3A%2F%2Fpurl.org%2Fnet%2Fmlo%2F%3E%0D%0APREFIX+aiiso%3A+%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Faiiso%2Fschema%23%3E%0D%0APREFIX+xcri%3A+%3Chttp%3A%2F%2Fxcri.org%2Fprofiles%2F1.2%2F%3E%0D%0APREFIX+coursesData%3A+%3Chttp%3A%2F%2Fdata.open.ac.uk%2Fcourse%2F%3E%0D%0A%0D%0ASELECT+%3Fcourse+%3Ftitle+%3Fdescription+%3Furl+WHERE+%7B%0D%0A++%3Fcourse+a+xcri%3Acourse+.%0D%0A++%3Fcourse+rdfs%3Alabel+%3Ftitle+.%0D%0A++OPTIONAL+%7B+%3Fcourse+xcri%3Adescription+%3Fdescription+%7D%0D%0A++OPTIONAL+%7B+%3Fcourse+mlo%3Aurl+%3Furl+%7D%0D%0A%7D%0D%0ALIMIT+50&_implicit=false&implicit=true&_form=%2Fsparql"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            saved_courses = []
            for course_data in data.get('results', {}).get('bindings', []):
                try:
                    course_uri = course_data.get('course', {}).get('value', '')
                    course_code = course_uri.split('/')[-1] if course_uri else f"OU-{len(saved_courses) + 1}"
                    
                    # Create course object
                    course = Course(
                        title=course_data.get('title', {}).get('value', 'Untitled Open University Course'),
                        code=course_code,
                        description=course_data.get('description', {}).get('value', '')[:500] if course_data.get('description') else '',
                        credits=random.randint(3, 6),  # Add required credits field
                        max_students=random.randint(30, 100),  # Add required max_students field
                        instructor='Open University Faculty',
                        website_link=course_data.get('url', {}).get('value', 'https://open.ac.uk/') if course_data.get('url') else 'https://open.ac.uk/',
                        difficulty_level=random.choice(['beginner', 'intermediate', 'advanced']),
                        status=random.choice(['upcoming', 'ongoing', 'completed']),
                        rating=round(random.uniform(3.5, 5.0), 1),
                        total_ratings=random.randint(10, 500),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    course.save()
                    saved_courses.append(course)
                    
                    # Add videos for this course
                    self._add_course_videos(course)
                    
                except Exception as e:
                    logger.error(f"Error saving Open University course: {str(e)}")
                    continue
                    
            return saved_courses
            
        except Exception as e:
            logger.error(f"Error fetching courses from Open University API: {str(e)}")
            self.stdout.write(self.style.WARNING(f'Failed to fetch courses from Open University API: {str(e)}'))
            return []
    
    def fetch_udacity_courses(self):
        """Fetch courses from Udacity's public catalog API"""
        api_url = "https://www.udacity.com/api/courses/v1/public-courses"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            saved_courses = []
            for course_data in data.get('courses', [])[:30]:  # Limit to 30 courses
                try:
                    instructors = [instructor.get('name', '') for instructor in course_data.get('instructors', [])]
                    instructor_names = ', '.join(instructors) if instructors else 'Udacity Instructor'
                    
                    # Map difficulty level
                    level = 'beginner'
                    if course_data.get('level') == 'intermediate':
                        level = 'intermediate'
                    elif course_data.get('level') == 'advanced':
                        level = 'advanced'
                    
                    # Create course object
                    course = Course(
                        title=course_data.get('title', 'Untitled Udacity Course'),
                        code=course_data.get('key', f"UD-{len(saved_courses) + 1}"),
                        description=course_data.get('short_summary', '')[:500] if course_data.get('short_summary') else '',
                        credits=random.randint(3, 6),  # Add required credits field
                        max_students=random.randint(30, 100),  # Add required max_students field
                        instructor=instructor_names,
                        website_link=f"https://www.udacity.com{course_data.get('url', '')}",
                        difficulty_level=level,
                        status='ongoing',  # Udacity courses are generally ongoing
                        rating=course_data.get('avg_rating', 4.0),
                        total_ratings=course_data.get('num_reviews', random.randint(10, 200)),
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    course.save()
                    saved_courses.append(course)
                    
                    # Add videos for this course
                    self._add_course_videos(course)
                    
                except Exception as e:
                    logger.error(f"Error saving Udacity course: {str(e)}")
                    continue
                    
            return saved_courses
            
        except Exception as e:
            logger.error(f"Error fetching courses from Udacity API: {str(e)}")
            self.stdout.write(self.style.WARNING(f'Failed to fetch courses from Udacity API: {str(e)}'))
            return []
    
    def create_mock_courses(self, num_courses=20):
        """Create mock courses when API calls fail or return insufficient data"""
        course_subjects = [
            "Python Programming", "Web Development", "Data Science", "Machine Learning",
            "Artificial Intelligence", "Mobile App Development", "Cloud Computing",
            "Cybersecurity", "Blockchain", "Game Development", "Digital Marketing",
            "UX/UI Design", "Project Management", "Business Analytics", "DevOps",
            "Software Engineering", "Network Administration", "Database Management",
            "Big Data", "Internet of Things"
        ]
        
        course_descriptions = [
            "Learn the fundamentals and advanced concepts of this subject area.",
            "A comprehensive course covering theory and practice with hands-on projects.",
            "Master essential skills through practical exercises and real-world examples.",
            "From beginner to expert: develop your skills with industry-standard tools.",
            "A project-based approach to learning with expert instruction and mentorship."
        ]
        
        instructors = [
            "Dr. Jane Smith", "Prof. John Davis", "Sarah Johnson, PhD", 
            "Michael Brown, Industry Expert", "Amanda Wilson & Team",
            "Dr. Robert Chen", "Emily Parker, Senior Engineer", "David Thompson, Tech Lead"
        ]
        
        universities = ["MIT", "Stanford", "Harvard", "Berkeley", "Oxford", "Cambridge", "Princeton"]
        
        saved_courses = []
        for i in range(num_courses):
            subject = random.choice(course_subjects)
            level = random.choice(["beginner", "intermediate", "advanced"])
            status = random.choice(["upcoming", "ongoing", "completed"])
            university = random.choice(universities)
            
            course = Course(
                title=f"{subject} {'Fundamentals' if level == 'beginner' else 'Advanced' if level == 'advanced' else 'Intermediate'}",
                code=f"MOCK-{i+1:03d}",
                description=f"{random.choice(course_descriptions)} This {level} {subject.lower()} course is offered by {university} University.",
                credits=random.randint(3, 6),  # Add required credits field
                max_students=random.randint(30, 100),  # Add required max_students field
                instructor=random.choice(instructors),
                website_link=f"https://example.com/courses/{subject.lower().replace(' ', '-')}",
                difficulty_level=level,
                status=status,
                rating=round(random.uniform(3.8, 5.0), 1),
                total_ratings=random.randint(50, 1000),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            course.save()
            saved_courses.append(course)
            
            # Add videos for this course
            self._add_course_videos(course)
            
        return saved_courses
        
    def _add_course_videos(self, course):
        """Add videos to a course using YouTube API"""
        # Get videos from YouTube API based on course title/topic
        search_query = self._generate_search_query(course)
        videos = self._search_youtube_videos(search_query, max_results=6)
        
        # Generic lesson titles based on difficulty level
        lesson_titles = {
            'beginner': [
                'Introduction and Course Overview', 
                'Getting Started with the Basics', 
                'Understanding Fundamental Concepts',
                'Building Your First Project',
                'Common Mistakes and How to Avoid Them'
            ],
            'intermediate': [
                'Advanced Techniques and Patterns', 
                'Optimizing Your Workflow', 
                'Integrating with External Systems',
                'Troubleshooting and Debugging',
                'Building Real-World Applications'
            ],
            'advanced': [
                'Expert-Level Strategies', 
                'Architecture and System Design', 
                'Performance Optimization',
                'Security Best Practices',
                'Enterprise-Grade Solutions'
            ]
        }
        
        # Use all videos we received from YouTube API
        selected_videos = videos if videos else []
        
        # Get appropriate lesson titles based on course difficulty
        titles = lesson_titles.get(course.difficulty_level, lesson_titles['beginner'])
        if len(titles) < num_videos:
            # If we need more titles than available, add generic ones
            titles.extend([f'Lesson {i+1}' for i in range(len(titles), num_videos)])
        
        # Create videos for this course
        for i, video_data in enumerate(selected_videos):
            try:
                # Create a course video
                lesson_title = titles[i] if i < len(titles) else f'Lesson {i+1}'
                video = CourseVideo(
                    course=course,
                    title=f"{lesson_title} - {video_data['title']}",
                    description=video_data.get('description', f"Learn about {lesson_title.lower()} in this comprehensive video."),
                    youtube_video_id=video_data['id'],
                    order=i+1
                )
                video.save()
            except Exception as e:
                logger.error(f"Error adding video to course {course.code}: {str(e)}")
                continue
                
    def _generate_search_query(self, course):
        """Generate a relevant search query for YouTube based on the course information"""
        # Extract main topic from course title
        title_words = course.title.split()
        # Remove common words
        common_words = ['course', 'introduction', 'fundamentals', 'advanced', 'intermediate', 'to', 'and', 'the', 'for']
        topic_words = [word for word in title_words if word.lower() not in common_words]
        
        if not topic_words and 'description' in course.__dict__:
            # Try to get topic from description
            desc_words = course.description.split()[:5]  # Use first 5 words of description
            topic_words = [word for word in desc_words if word.lower() not in common_words]
        
        # Fallback if no meaningful words found
        if not topic_words:
            topic_words = ['programming', 'tutorial']
            
        # Add difficulty level and educational terms
        query_parts = topic_words[:2]  # Use at most 2 topic words to keep query focused
        query_parts.append(course.difficulty_level)
        query_parts.append('tutorial')
        
        return ' '.join(query_parts)
    
    def _search_youtube_videos(self, query, max_results=6):
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
            'videoDefinition': 'high'  # High definition videos
        }
        
        try:
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
                        'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
                    })
            
            self.stdout.write(f"Found {len(videos)} videos for query: '{query}'")
            return videos
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"YouTube API error: {str(e)}. Using fallback video data."))
            # Fallback to some predefined videos if API fails
            return self._get_fallback_videos()
    
    def _get_fallback_videos(self):
        """Return fallback video data if YouTube API fails"""
        return [
            {'id': 'rfscVS0vtbw', 'title': 'Learn Python - Full Course for Beginners', 'description': 'Comprehensive introduction to Python programming'},
            {'id': '_uQrJ0TkZlc', 'title': 'Python Tutorial - Python Full Course for Beginners', 'description': 'Learn Python programming with hands-on exercises'},
            {'id': 'Z1Yd7upQsXY', 'title': 'Python Tutorial for Absolute Beginners', 'description': 'Step-by-step guide to Python for beginners'},
            {'id': 'qz0aGYrrlhU', 'title': 'HTML Tutorial for Beginners', 'description': 'Learn HTML from scratch with this comprehensive tutorial'},
            {'id': 'W6NZfCO5SIk', 'title': 'JavaScript Tutorial for Beginners', 'description': 'Start your journey with JavaScript programming'}            
        ]
