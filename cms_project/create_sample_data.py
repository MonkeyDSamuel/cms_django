#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms_project.settings')
django.setup()

from labtech_backend_app.models import Category, Test

def create_sample_data():
    print("Creating sample data for lab technician app...")
    
    # Create categories
    categories_data = [
        "Blood Tests",
        "Urine Tests", 
        "Microbiology",
        "Biochemistry",
        "Hematology",
        "Immunology"
    ]
    
    created_categories = []
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(category_name=cat_name)
        created_categories.append(category)
        print(f"Category: {cat_name} - {'Created' if created else 'Already exists'}")
    
    # Create sample tests
    tests_data = [
        {
            "test_name": "Complete Blood Count (CBC)",
            "category": "Blood Tests",
            "rate": 150.00,
            "min_value": 4.0,
            "max_value": 11.0
        },
        {
            "test_name": "Blood Glucose (Fasting)",
            "category": "Blood Tests", 
            "rate": 80.00,
            "min_value": 70.0,
            "max_value": 100.0
        },
        {
            "test_name": "Urine Analysis",
            "category": "Urine Tests",
            "rate": 60.00
        },
        {
            "test_name": "Blood Culture",
            "category": "Microbiology",
            "rate": 200.00
        },
        {
            "test_name": "Liver Function Test",
            "category": "Biochemistry",
            "rate": 300.00
        },
        {
            "test_name": "Hemoglobin A1C",
            "category": "Blood Tests",
            "rate": 120.00,
            "min_value": 4.0,
            "max_value": 6.0
        },
        {
            "test_name": "Thyroid Function Test",
            "category": "Blood Tests",
            "rate": 250.00
        },
        {
            "test_name": "Stool Culture",
            "category": "Microbiology",
            "rate": 180.00
        },
        {
            "test_name": "Lipid Profile",
            "category": "Blood Tests",
            "rate": 200.00
        },
        {
            "test_name": "Kidney Function Test",
            "category": "Biochemistry",
            "rate": 280.00
        }
    ]
    
    for test_data in tests_data:
        category = Category.objects.get(category_name=test_data["category"])
        test, created = Test.objects.get_or_create(
            test_name=test_data["test_name"],
            defaults={
                "category": category,
                "rate": test_data["rate"],
                "min_value": test_data.get("min_value"),
                "max_value": test_data.get("max_value"),
                "is_active": True
            }
        )
        print(f"Test: {test_data['test_name']} - {'Created' if created else 'Already exists'}")
    
    print(f"\nSample data creation completed!")
    print(f"Total Categories: {Category.objects.count()}")
    print(f"Total Tests: {Test.objects.count()}")

if __name__ == "__main__":
    create_sample_data()
