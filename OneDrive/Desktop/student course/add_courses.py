import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

from courses.models import Course

courses_data = [
    {
        'title': 'Introduction to Python Programming',
        'code': 'CS101',
        'description': 'Learn the basics of Python programming language including variables, data types, control structures, functions, and object-oriented programming.',
        'credits': 3,
        'instructor': 'Dr. John Smith',
        'max_students': 30,
        'website_link': 'https://www.python.org/about/gettingstarted/'
    },
    {
        'title': 'Web Development with Django',
        'code': 'CS201',
        'description': 'Learn web development using Django framework. Topics include MVT architecture, forms, authentication, and database management.',
        'credits': 4,
        'instructor': 'Prof. Sarah Johnson',
        'max_students': 25,
        'website_link': 'https://www.djangoproject.com/start/'
    },
    {
        'title': 'Data Science Fundamentals',
        'code': 'DS101',
        'description': 'Introduction to data science concepts including data analysis, visualization, and basic machine learning using Python libraries.',
        'credits': 4,
        'instructor': 'Dr. Michael Brown',
        'max_students': 20,
        'website_link': 'https://pandas.pydata.org/docs/getting_started/'
    },
    {
        'title': 'JavaScript and React',
        'code': 'WD301',
        'description': 'Master modern JavaScript and React framework for building interactive web applications.',
        'credits': 3,
        'instructor': 'Prof. Emily Davis',
        'max_students': 25,
        'website_link': 'https://react.dev/learn'
    },
    {
        'title': 'Database Management Systems',
        'code': 'DB201',
        'description': 'Learn about database design, SQL, normalization, and database management systems.',
        'credits': 3,
        'instructor': 'Dr. Robert Wilson',
        'max_students': 30,
        'website_link': 'https://www.postgresql.org/docs/current/tutorial.html'
    }
]

def add_courses():
    for course_data in courses_data:
        try:
            Course.objects.create(**course_data)
            print(f"Added course: {course_data['title']}")
        except Exception as e:
            print(f"Error adding course {course_data['title']}: {str(e)}")

if __name__ == '__main__':
    print("Adding courses...")
    add_courses()
    print("Finished adding courses!") 