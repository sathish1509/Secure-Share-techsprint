from django.core.management.base import BaseCommand
from django.conf import settings
from courses.models import Course
from accounts.coursera_api import get_coursera_courses, get_coursera_access_token
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Delete all existing courses and fetch fresh courses from Coursera API'

    def handle(self, *args, **options):
        self.stdout.write('Starting course update process...')
        
        # Delete all existing courses
        self.stdout.write('Deleting existing courses...')
        Course.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All existing courses deleted'))

        # Get access token
        self.stdout.write('Getting access token from Coursera API...')
        token_data = get_coursera_access_token()
        if not token_data or 'access_token' not in token_data:
            self.stdout.write(self.style.ERROR('Failed to get access token from Coursera API'))
            return

        access_token = token_data['access_token']
        
        # Fetch courses
        self.stdout.write('Fetching courses from Coursera API...')
        courses_data = get_coursera_courses(access_token)
        if not courses_data or 'elements' not in courses_data:
            self.stdout.write(self.style.ERROR('Failed to fetch courses from Coursera API'))
            return

        courses = courses_data['elements']
        total_courses = 0
        
        for course_data in courses:
            try:
                # Create new course
                course = Course(
                    title=course_data.get('name', 'Untitled Course'),
                    code=course_data.get('id', ''),
                    description=course_data.get('shortDescription', ''),
                    instructor=', '.join([instructor.get('name', '') 
                                        for instructor in course_data.get('instructors', [])]),
                    website_link=f"https://www.coursera.org/learn/{course_data.get('slug', '')}",
                    difficulty_level=self._map_difficulty(course_data.get('difficulty', '')),
                    status=self._map_status(course_data.get('status', '')),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                # Add rating if available
                rating = course_data.get('averageRating', 0)
                if rating:
                    course.rating = float(rating)
                    course.total_ratings = course_data.get('numRatings', 0)
                
                course.save()
                total_courses += 1
                
            except Exception as e:
                logger.error(f"Error saving course {course_data.get('id', '')}: {str(e)}")
                continue

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched {total_courses} courses'))

    def _map_difficulty(self, difficulty):
        """Map Coursera difficulty to our model choices"""
        difficulty_map = {
            'beginner': 'beginner',
            'intermediate': 'intermediate',
            'advanced': 'advanced'
        }
        return difficulty_map.get(difficulty.lower(), 'beginner')

    def _map_status(self, status):
        """Map Coursera status to our model choices"""
        status_map = {
            'launching': 'upcoming',
            'active': 'ongoing',
            'completed': 'completed'
        }
        return status_map.get(status.lower(), 'upcoming')
