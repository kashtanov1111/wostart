import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import random
from tags.models import Tag
from faker import Faker

fakegen = Faker()

# def populate(N=10):

#     for i in range(N):
#         fake_company_name = fakegen.company()
#         COMPANY = Company.objects.get_or_create(company_name=fake_company_name)[0]

#     COMPANY = Company.objects.order_by('company_name')

#     for i in range(3):
#         for j in range(len(COMPANY)):
#             fake_first_name = fakegen.first_name()
#             fake_last_name = fakegen.last_name()
#             WORKER = Worker.objects.get_or_create(company=COMPANY[j], first_name=fake_first_name, last_name=fake_last_name)[0]

# def populate2(N=30):

#     for i in range(N):
#         fake_first_name = fakegen.first_name()
#         fake_last_name = fakegen.last_name()
#         fake_email = fakegen.email()
#         USER = User.objects.get_or_create(first_name=fake_first_name, last_name=fake_last_name, email=fake_email)

if __name__ == '__main__':
    print('start')
    print(fakegen.name())
    print('finish')