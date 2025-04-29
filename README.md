[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hLqvXyMi)

# Live Server
https://supplysite-20c1e0704260.herokuapp.com

Please use a virtual environment. After cloning, run:
1. cd .\project-a-28\
2. py -m venv .venv
3. .venv\Scripts\activate (**Windows**) OR source .venv/bin/activate (**MacOs**)
4. pip install -r requirements.txt
5. python manage.py runserver

Note that you automatically connect to the live database, even when running locally.
The main branch has Amazon S3 configured, which cannot be accessed locally. Profile Pictures and Item Pictures will not appear locally.

# Member Contributions
1. Zaid Contractor
- Role: Scrum Master
- Compiled sprint reports and presented our progress to the TA
- Led team meetings, communication, efforts, testing schemes, and development progress
- Shared key personal insights about the entire development progress in the Scrum Master Report
- Developer contributions: login page, anonymous users page, integration of marketplace and home page, major UI improvements across the app, debugging various features
2. Rory Kretzer
- Role: Requirements Manager
- Led requirements elicitation process and compiled a comprehensive report
- Initial setup of the app's homepage, and navbar
- All functionality pertaining to reviews and ratings for both users and items + My Reviews page
- Models for Items, tags, and classes
- Required materials page (new UI was not me)
- Librarian requests page
- Requesting access to collections
- Marking items as returned
- Various Debugging Tasks
4. Surya Vemulapalli
- Role: Testing Manager
- 
5. Aidan Szilagyi
- Role: DevOps Manager
- 
6. Dev Patel
- Role: Software Architect
-   

# Licenses for Major Libraries/Frameworks
| Library / Framework         | License        | URL                            |
|----------------------------|----------------|---------------------------------|
| Django                     | BSD-3          | [Link](https://github.com/django/django/blob/master/LICENSE) |
| django-allauth            | MIT            | [Link](https://github.com/pennersr/django-allauth/blob/master/LICENSE) |
| gunicorn                   | MIT            | [Link](https://github.com/benoitc/gunicorn/blob/master/LICENSE) |
| psycopg2-binary            | LGPL-3.0       | [Link](https://www.psycopg.org/license/) |
| whitenoise                 | MIT            | [Link](https://github.com/evansd/whitenoise/blob/main/LICENSE) |
| Pillow                     | HPND           | [Link](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| django-storages           | BSD-3-Clause   | [Link](https://github.com/jschneier/django-storages/blob/master/LICENSE) |
| boto3                      | Apache-2.0     | [Link](https://github.com/boto/boto3/blob/develop/LICENSE) |
| social-auth-app-django     | BSD-3-Clause   | [Link](https://github.com/python-social-auth/social-app-django/blob/master/LICENSE) |
| celery                     | BSD-3-Clause   | [Link](https://github.com/celery/celery/blob/main/LICENSE) |
| djangorestframework        | BSD-3-Clause   | [Link](https://github.com/encode/django-rest-framework/blob/master/LICENSE.md) |

# Licensing Suggestions
Given that our project is a Django-based cataloging and lending application, and considering the licenses of the dependencies (primarily permissive licenses like MIT, BSD, and Apache 2.0), releasing our project under the MIT License would be a suitable choice. The MIT License is widely used, simple, and permissive, allowing others to use, modify, and distribute our code with minimal restrictions.
