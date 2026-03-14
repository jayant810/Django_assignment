from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Vendors
        v1 = Vendor.objects.get_or_create(name='Global Solutions', code='VEN001', description='Global tech solutions')[0]
        v2 = Vendor.objects.get_or_create(name='Quality Systems', code='VEN002', description='Systems quality assurance')[0]

        # Create Products
        p1 = Product.objects.get_or_create(name='TechPlus ERP', code='PRD001', description='Enterprise Resource Planning')[0]
        p2 = Product.objects.get_or_create(name='SecureNet VPN', code='PRD002', description='Virtual Private Network')[0]
        p3 = Product.objects.get_or_create(name='DataAnalyzer', code='PRD003', description='Big Data Analysis tool')[0]

        # Create Courses
        c1 = Course.objects.get_or_create(name='ERP Implementation', code='CRS001', description='Mastering ERP setup')[0]
        c2 = Course.objects.get_or_create(name='Network Security 101', code='CRS002', description='Basics of network security')[0]
        c3 = Course.objects.get_or_create(name='Advanced Data Mining', code='CRS003', description='Data mining techniques')[0]

        # Create Certifications
        cert1 = Certification.objects.get_or_create(name='Certified ERP Specialist', code='CRT001', description='Specialist in ERP')[0]
        cert2 = Certification.objects.get_or_create(name='Network Security Professional', code='CRT002', description='Pro in network security')[0]
        cert3 = Certification.objects.get_or_create(name='Data Science Expert', code='CRT003', description='Expert in data science')[0]

        # Create Mappings
        # Vendor -> Product
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p1, primary_mapping=True)
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p2, primary_mapping=False)
        VendorProductMapping.objects.get_or_create(vendor=v2, product=p3, primary_mapping=True)

        # Product -> Course
        ProductCourseMapping.objects.get_or_create(product=p1, course=c1, primary_mapping=True)
        ProductCourseMapping.objects.get_or_create(product=p2, course=c2, primary_mapping=True)
        ProductCourseMapping.objects.get_or_create(product=p3, course=c3, primary_mapping=True)

        # Course -> Certification
        CourseCertificationMapping.objects.get_or_create(course=c1, certification=cert1, primary_mapping=True)
        CourseCertificationMapping.objects.get_or_create(course=c2, certification=cert2, primary_mapping=True)
        CourseCertificationMapping.objects.get_or_create(course=c3, certification=cert3, primary_mapping=True)

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
