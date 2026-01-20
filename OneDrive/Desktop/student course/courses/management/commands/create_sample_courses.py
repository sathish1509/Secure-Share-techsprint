from django.core.management.base import BaseCommand
from django.utils import timezone
from courses.models import Course
from datetime import timedelta

class Command(BaseCommand):
    help = 'Creates sample courses for demonstration'

    def handle(self, *args, **kwargs):
        courses_data = [
            {
                'title': 'Introduction to Python Programming',
                'code': 'CS101',
                'description': 'A comprehensive introduction to Python programming language covering basics to advanced concepts.',
                'credits': 3,
                'instructor': 'Dr. John Smith',
                'max_students': 30,
                'difficulty_level': 'beginner',
                'prerequisites': 'No prior programming experience required',
                'syllabus': '1. Python Basics\n2. Control Flow\n3. Functions\n4. Data Structures\n5. Object-Oriented Programming',
                'learning_outcomes': '- Write basic Python programs\n- Understand core programming concepts\n- Implement simple algorithms',
            },
            {
                'title': 'Web Development with Django',
                'code': 'CS201',
                'description': 'Learn to build web applications using Django framework with best practices.',
                'credits': 4,
                'instructor': 'Prof. Sarah Johnson',
                'max_students': 25,
                'difficulty_level': 'intermediate',
                'prerequisites': 'Basic Python knowledge, HTML/CSS fundamentals',
                'syllabus': '1. Django Basics\n2. Models and Databases\n3. Views and Templates\n4. Forms and Authentication\n5. REST APIs',
                'learning_outcomes': '- Build full-stack web applications\n- Implement authentication systems\n- Deploy Django applications',
            },
            {
                'title': 'Machine Learning Fundamentals',
                'code': 'AI301',
                'description': 'Introduction to machine learning concepts, algorithms, and practical applications.',
                'credits': 4,
                'instructor': 'Dr. Michael Chen',
                'max_students': 20,
                'difficulty_level': 'advanced',
                'prerequisites': 'Python programming, Basic statistics, Linear algebra',
                'syllabus': '1. Supervised Learning\n2. Unsupervised Learning\n3. Neural Networks\n4. Model Evaluation\n5. Project Implementation',
                'learning_outcomes': '- Implement ML algorithms\n- Evaluate model performance\n- Solve real-world ML problems',
            },
            {
                'title': 'Mobile App Development',
                'code': 'MOB401',
                'description': 'Learn to develop cross-platform mobile applications using React Native.',
                'credits': 3,
                'instructor': 'Prof. Emily Williams',
                'max_students': 25,
                'difficulty_level': 'intermediate',
                'prerequisites': 'JavaScript fundamentals, React basics',
                'syllabus': '1. React Native Basics\n2. Navigation\n3. State Management\n4. Native Modules\n5. App Deployment',
                'learning_outcomes': '- Build mobile applications\n- Implement responsive UI\n- Deploy to app stores',
            },
        ]

        today = timezone.now().date()
        
        for course_data in courses_data:
            course = Course.objects.create(
                **course_data,
                start_date=today,
                end_date=today + timedelta(days=90),
                status='ongoing'
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created course: {course.code}')) 