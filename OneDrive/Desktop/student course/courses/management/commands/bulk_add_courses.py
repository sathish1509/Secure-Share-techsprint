import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from courses.models import Course
from datetime import timedelta

class Command(BaseCommand):
    help = 'Bulk add 200 unique sample courses.'

    def handle(self, *args, **kwargs):
        titles = [
            'Python', 'Django', 'Machine Learning', 'Data Science', 'Web Development', 'Mobile Apps',
            'Cloud Computing', 'Cybersecurity', 'Blockchain', 'UI/UX Design', 'DevOps', 'Game Development',
            'JavaScript', 'React', 'Angular', 'Vue', 'C++', 'Java', 'Kotlin', 'Swift', 'Flutter', 'AWS',
            'Azure', 'GCP', 'Linux', 'Docker', 'Kubernetes', 'SQL', 'NoSQL', 'Big Data', 'AI', 'NLP',
            'Computer Vision', 'Robotics', 'IoT', 'Networking', 'Algorithms', 'Data Structures', 'Testing',
            'Agile', 'Scrum', 'Project Management', 'Business Analysis', 'Finance', 'Marketing', 'Sales',
            'HR', 'Leadership', 'Communication', 'Writing', 'Public Speaking', 'Photography', 'Video Editing',
            'Music Production', 'Animation', '3D Modeling', 'AR/VR', 'Ethical Hacking', 'Penetration Testing',
            'Forensics', 'Compliance', 'Risk Management', 'SaaS', 'PaaS', 'IaaS', 'Edge Computing', 'Quantum Computing',
            'Bioinformatics', 'Genomics', 'Healthcare IT', 'EdTech', 'LegalTech', 'InsurTech', 'FinTech', 'Sports Analytics',
            'E-commerce', 'Retail Analytics', 'Supply Chain', 'Logistics', 'Operations', 'Customer Service', 'Support',
            'Content Creation', 'SEO', 'SEM', 'Social Media', 'Branding', 'Graphic Design', 'Illustration', 'Fashion',
            'Interior Design', 'Architecture', 'Civil Engineering', 'Mechanical Engineering', 'Electrical Engineering',
            'Chemical Engineering', 'Environmental Science', 'Geology', 'Astronomy', 'Physics', 'Mathematics', 'Statistics',
            'Biology', 'Chemistry', 'Psychology', 'Sociology', 'Philosophy', 'History', 'Political Science', 'Economics',
            'Anthropology', 'Linguistics', 'Languages', 'Education', 'Teaching', 'Coaching', 'Fitness', 'Nutrition',
            'Wellness', 'Personal Development', 'Mindfulness', 'Meditation', 'Yoga', 'Travel', 'Tourism', 'Hospitality',
            'Culinary Arts', 'Baking', 'Bartending', 'Wine Tasting', 'Gardening', 'Horticulture', 'Agriculture', 'Animal Science',
            'Veterinary Science', 'Zoology', 'Marine Biology', 'Oceanography', 'Meteorology', 'Climatology', 'Geography',
            'Urban Planning', 'Real Estate', 'Property Management', 'Investing', 'Trading', 'Cryptocurrency', 'Blockchain',
            'Smart Contracts', 'Drones', 'Aviation', 'Piloting', 'Navigation', 'Sailing', 'Boating', 'Fishing', 'Hiking',
            'Camping', 'Survival Skills', 'First Aid', 'Emergency Management', 'Disaster Recovery', 'Security', 'Law Enforcement',
            'Military Science', 'Defense', 'Strategy', 'Game Theory', 'Chess', 'Board Games', 'Card Games', 'Esports', 'Streaming',
            'Podcasting', 'Blogging', 'Vlogging', 'Influencer Marketing', 'Affiliate Marketing', 'Dropshipping', 'Print on Demand',
            'Freelancing', 'Consulting', 'Entrepreneurship', 'Startups', 'Innovation', 'Product Management', 'Design Thinking',
            'Lean Startup', 'Growth Hacking', 'Customer Success', 'User Research', 'A/B Testing', 'Conversion Optimization',
            'Mobile Marketing', 'App Store Optimization', 'Email Marketing', 'Copywriting', 'Editing', 'Proofreading', 'Translation',
            'Localization', 'Transcription', 'Voice Acting', 'Acting', 'Directing', 'Screenwriting', 'Film Production', 'Cinematography',
            'Lighting', 'Sound Design', 'Set Design', 'Costume Design', 'Makeup', 'Hair Styling', 'Stunt Work', 'Special Effects',
            'Motion Graphics', 'Stop Motion', 'Claymation', 'Puppetry', 'Magic', 'Circus Arts', 'Dance', 'Ballet', 'Jazz', 'Hip Hop',
            'Tap', 'Ballroom', 'Latin', 'Folk', 'World Music', 'Classical Music', 'Opera', 'Choir', 'Orchestra', 'Band', 'Solo Performance',
            'Songwriting', 'Composing', 'Arranging', 'Conducting', 'Music Theory', 'Ear Training', 'Sight Reading', 'Improvisation',
            'Music History', 'Music Business', 'Music Technology', 'Sound Engineering', 'Live Sound', 'Studio Recording', 'Mixing', 'Mastering',
            'DJing', 'Turntablism', 'Beatboxing', 'Rapping', 'Spoken Word', 'Poetry', 'Storytelling', 'Creative Writing', 'Fiction', 'Nonfiction',
            'Memoir', 'Biography', 'Autobiography', 'Journalism', 'News Writing', 'Investigative Reporting', 'Photojournalism', 'War Reporting',
            'Science Writing', 'Technical Writing', 'Grant Writing', 'Proposal Writing', 'Business Writing', 'Academic Writing', 'Research',
            'Data Analysis', 'Data Visualization', 'Infographics', 'Presentation Skills', 'Public Relations', 'Media Relations', 'Crisis Communication',
            'Event Planning', 'Fundraising', 'Volunteer Management', 'Nonprofit Management', 'Advocacy', 'Lobbying', 'Campaign Management',
            'Polling', 'Survey Design', 'Market Research', 'Consumer Behavior', 'Brand Management', 'Product Development', 'Quality Assurance',
            'Testing', 'Inspection', 'Compliance', 'Regulation', 'Policy Analysis', 'Risk Assessment', 'Insurance', 'Claims Management', 'Underwriting',
            'Actuarial Science', 'Retirement Planning', 'Estate Planning', 'Tax Planning', 'Financial Planning', 'Wealth Management', 'Asset Management',
            'Portfolio Management', 'Investment Banking', 'Corporate Finance', 'Mergers & Acquisitions', 'Venture Capital', 'Private Equity', 'Hedge Funds',
            'Real Assets', 'Commodities', 'Futures', 'Options', 'Derivatives', 'Fixed Income', 'Equities', 'Mutual Funds', 'ETFs', 'REITs', 'Trusts',
            'Foundations', 'Endowments', 'Philanthropy', 'Charity', 'Social Enterprise', 'Impact Investing', 'Sustainable Investing', 'ESG', 'CSR',
            'Green Finance', 'Climate Finance', 'Carbon Markets', 'Renewable Energy', 'Energy Efficiency', 'Clean Tech', 'Smart Grid', 'Electric Vehicles',
            'Battery Technology', 'Hydrogen', 'Nuclear Energy', 'Oil & Gas', 'Mining', 'Metals', 'Materials', 'Chemicals', 'Plastics', 'Textiles',
            'Paper', 'Packaging', 'Printing', 'Publishing', 'Advertising', 'Media Buying', 'Media Planning', 'Broadcasting', 'Television', 'Radio',
            'Film', 'Video', 'Animation', 'Games', 'Apps', 'Software', 'Hardware', 'Electronics', 'Robotics', 'Automation', 'Sensors', 'Actuators',
            'Embedded Systems', 'Wearables', 'Smart Home', 'Smart Cities', 'Internet of Things', 'Connected Devices', 'Edge Devices', 'Fog Computing',
            'Mesh Networks', 'Wireless', 'Bluetooth', 'Wi-Fi', 'Zigbee', 'LoRa', '5G', 'Satellite', 'Space', 'Astronautics', 'Rocketry', 'Astrophysics',
            'Cosmology', 'Exoplanets', 'Astrobiology', 'SETI', 'Space Exploration', 'Space Tourism', 'Space Mining', 'Space Law', 'Space Policy',
            'Space Business', 'Space Entrepreneurship', 'Space Startups', 'Space Investment', 'Space Technology', 'Space Science', 'Space Engineering',
            'Space Medicine', 'Space Psychology', 'Space Sociology', 'Space Philosophy', 'Space History', 'Space Art', 'Space Music', 'Space Literature',
            'Space Film', 'Space TV', 'Space Games', 'Space Apps', 'Space Software', 'Space Hardware', 'Space Robotics', 'Space Automation', 'Space Sensors',
            'Space Actuators', 'Space Embedded Systems', 'Space Wearables', 'Space Smart Home', 'Space Smart Cities', 'Space Internet of Things',
            'Space Connected Devices', 'Space Edge Devices', 'Space Fog Computing', 'Space Mesh Networks', 'Space Wireless', 'Space Bluetooth', 'Space Wi-Fi',
            'Space Zigbee', 'Space LoRa', 'Space 5G', 'Space Satellite', 'Space Space', 'Space Astronautics', 'Space Rocketry', 'Space Astrophysics',
            'Space Cosmology', 'Space Exoplanets', 'Space Astrobiology', 'Space SETI', 'Space Space Exploration', 'Space Space Tourism', 'Space Space Mining',
            'Space Space Law', 'Space Space Policy', 'Space Space Business', 'Space Space Entrepreneurship', 'Space Space Startups', 'Space Space Investment',
            'Space Space Technology', 'Space Space Science', 'Space Space Engineering', 'Space Space Medicine', 'Space Space Psychology', 'Space Space Sociology',
            'Space Space Philosophy', 'Space Space History', 'Space Space Art', 'Space Space Music', 'Space Space Literature', 'Space Space Film', 'Space Space TV',
            'Space Space Games', 'Space Space Apps', 'Space Space Software', 'Space Space Hardware', 'Space Space Robotics', 'Space Space Automation', 'Space Space Sensors',
            'Space Space Actuators', 'Space Space Embedded Systems', 'Space Space Wearables', 'Space Space Smart Home', 'Space Space Smart Cities', 'Space Space Internet of Things',
            'Space Space Connected Devices', 'Space Space Edge Devices', 'Space Space Fog Computing', 'Space Space Mesh Networks', 'Space Space Wireless', 'Space Space Bluetooth',
            'Space Space Wi-Fi', 'Space Space Zigbee', 'Space Space LoRa', 'Space Space 5G', 'Space Space Satellite'
        ]
        instructors = [
            'Dr. John Smith', 'Prof. Sarah Johnson', 'Dr. Michael Chen', 'Prof. Emily Williams',
            'Dr. Alan Turing', 'Prof. Lisa Chen', 'Dr. Satoshi Nakamoto', 'Prof. Emma Design',
            'Dr. Jenkins Master', 'Prof. Mario Unity', 'Prof. Ada Lovelace', 'Prof. Grace Hopper',
            'Dr. Tim Berners-Lee', 'Prof. Donald Knuth', 'Dr. Linus Torvalds', 'Prof. Barbara Liskov',
            'Dr. Edsger Dijkstra', 'Prof. Margaret Hamilton', 'Dr. Dennis Ritchie', 'Prof. Brian Kernighan'
        ]
        today = timezone.now().date()
        for i in range(200):
            title = f"{random.choice(titles)} {random.randint(100,999)}"
            code = f"C{i+1:03d}"
            description = f"This is a sample course about {title}. It covers all the essentials and more."
            credits = random.choice([2, 3, 4, 5])
            instructor = random.choice(instructors)
            max_students = random.randint(20, 50)
            difficulty_level = random.choice(['beginner', 'intermediate', 'advanced'])
            prerequisites = "None required."
            syllabus = "1. Introduction\n2. Main Concepts\n3. Advanced Topics\n4. Project\n5. Review"
            learning_outcomes = "- Understand the basics\n- Apply concepts in real-world scenarios\n- Complete a capstone project"
            start_date = today
            end_date = today + timedelta(days=random.randint(60, 120))
            status = random.choice(['upcoming', 'ongoing', 'completed'])
            Course.objects.create(
                title=title,
                code=code,
                description=description,
                credits=credits,
                instructor=instructor,
                max_students=max_students,
                difficulty_level=difficulty_level,
                prerequisites=prerequisites,
                syllabus=syllabus,
                learning_outcomes=learning_outcomes,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
        self.stdout.write(self.style.SUCCESS('Successfully added 200 sample courses!')) 