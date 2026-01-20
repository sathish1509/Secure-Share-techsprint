from django.core.management.base import BaseCommand
from courses.models import Course, CourseVideo

class Command(BaseCommand):
    help = 'Adds sample educational videos to courses'

    def handle(self, *args, **kwargs):
        # Sample videos for different course types
        sample_videos = {
            'Python': [
                {
                    'title': 'Python for Beginners - Full Course',
                    'description': 'Learn Python programming from scratch with this comprehensive course.',
                    'youtube_video_id': 'kqtD5dpn9C8',
                    'order': 1
                },
                {
                    'title': 'Python OOP Tutorial',
                    'description': 'Object-oriented programming in Python explained with examples.',
                    'youtube_video_id': 'JeznW_7DlB0',
                    'order': 2
                }
            ],
            'Django': [
                {
                    'title': 'Django Tutorial for Beginners',
                    'description': 'Learn Django web framework from scratch.',
                    'youtube_video_id': 'F5mRW0jo-U4',
                    'order': 1
                },
                {
                    'title': 'Django REST Framework Tutorial',
                    'description': 'Building REST APIs with Django REST Framework.',
                    'youtube_video_id': 'c708Nf0cHrs',
                    'order': 2
                }
            ],
            'Web Development': [
                {
                    'title': 'HTML & CSS Full Course',
                    'description': 'Complete web development course covering HTML and CSS.',
                    'youtube_video_id': 'mU6anWqZJcc',
                    'order': 1
                },
                {
                    'title': 'JavaScript Tutorial for Beginners',
                    'description': 'Learn JavaScript programming from scratch.',
                    'youtube_video_id': 'W6NZfCO5SIk',
                    'order': 2
                }
            ],
            'Data Science': [
                {
                    'title': 'Data Science Full Course',
                    'description': 'Complete data science course with Python.',
                    'youtube_video_id': 'ua-CiDNNj30',
                    'order': 1
                },
                {
                    'title': 'Machine Learning Tutorial',
                    'description': 'Introduction to machine learning concepts and algorithms.',
                    'youtube_video_id': 'KNAWp2S3w94',
                    'order': 2
                }
            ]
        }

        # Add videos to courses based on their titles
        for course in Course.objects.all():
            course_title = course.title.lower()
            videos_added = 0

            for category, videos in sample_videos.items():
                if category.lower() in course_title:
                    for video_data in videos:
                        try:
                            CourseVideo.objects.create(
                                course=course,
                                title=video_data['title'],
                                description=video_data['description'],
                                youtube_video_id=video_data['youtube_video_id'],
                                order=video_data['order']
                            )
                            videos_added += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Error adding video to {course.title}: {str(e)}'
                                )
                            )

            if videos_added > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully added {videos_added} videos to {course.title}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'No matching videos found for {course.title}'
                    )
                ) 