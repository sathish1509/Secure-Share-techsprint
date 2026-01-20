import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

from courses.models import Course

additional_courses = [
    {
        'title': 'Machine Learning Fundamentals',
        'code': 'AI101',
        'description': 'Introduction to machine learning concepts, algorithms, and practical applications using Python and popular ML libraries.',
        'credits': 4,
        'instructor': 'Dr. Alan Turing',
        'max_students': 25,
        'website_link': 'https://www.coursera.org/learn/machine-learning'
    },
    {
        'title': 'Cybersecurity Essentials',
        'code': 'SEC201',
        'description': 'Learn fundamental concepts of cybersecurity, including network security, cryptography, and ethical hacking.',
        'credits': 3,
        'instructor': 'Prof. Lisa Chen',
        'max_students': 30,
        'website_link': 'https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/entry/security.html'
    },
    {
        'title': 'Mobile App Development with Flutter',
        'code': 'MOB301',
        'description': 'Build cross-platform mobile applications using Flutter and Dart programming language.',
        'credits': 4,
        'instructor': 'Dr. Sarah Miller',
        'max_students': 25,
        'website_link': 'https://flutter.dev/learn'
    },
    {
        'title': 'Cloud Computing with AWS',
        'code': 'CLD201',
        'description': 'Master cloud computing concepts and services using Amazon Web Services (AWS).',
        'credits': 3,
        'instructor': 'Prof. James Cloud',
        'max_students': 30,
        'website_link': 'https://aws.amazon.com/training/'
    },
    {
        'title': 'Blockchain Development',
        'code': 'BLC301',
        'description': 'Learn blockchain technology, smart contracts, and decentralized application development.',
        'credits': 4,
        'instructor': 'Dr. Satoshi Nakamoto',
        'max_students': 20,
        'website_link': 'https://ethereum.org/en/developers/'
    },
    {
        'title': 'UI/UX Design Principles',
        'code': 'DES201',
        'description': 'Master the principles of user interface and user experience design for digital products.',
        'credits': 3,
        'instructor': 'Prof. Emma Design',
        'max_students': 25,
        'website_link': 'https://www.interaction-design.org/courses'
    },
    {
        'title': 'DevOps and Automation',
        'code': 'DEV401',
        'description': 'Learn DevOps practices, CI/CD pipelines, and infrastructure automation.',
        'credits': 4,
        'instructor': 'Dr. Jenkins Master',
        'max_students': 20,
        'website_link': 'https://www.docker.com/get-started/'
    },
    {
        'title': 'Game Development with Unity',
        'code': 'GAM301',
        'description': 'Create interactive games using Unity game engine and C# programming.',
        'credits': 4,
        'instructor': 'Prof. Mario Unity',
        'max_students': 25,
        'website_link': 'https://learn.unity.com/'
    }
]

def add_more_courses():
    for course_data in additional_courses:
        try:
            Course.objects.create(**course_data)
            print(f"Added course: {course_data['title']}")
        except Exception as e:
            print(f"Error adding course {course_data['title']}: {str(e)}")

if __name__ == '__main__':
    print("Adding additional courses...")
    add_more_courses()
    print("Finished adding additional courses!") 