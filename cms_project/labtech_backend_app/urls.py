# from django.urls import path
# from .views import (
#     CategoryViewSet,
#     TestViewSet,
#     LabTestResultViewSet,
#     LabBillingViewSet,
# )

# category_list = CategoryViewSet.as_view({
#     "get": "list",
#     "post": "create",
# })
# category_detail = CategoryViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy",
# })

# test_list = TestViewSet.as_view({
#     "get": "list",
#     "post": "create",
# })
# test_detail = TestViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy",
# })
# tests_by_category = TestViewSet.as_view({
#     "get": "get_tests_by_category",
# })
# tests_search = TestViewSet.as_view({
#     "get": "search_tests",
# })
# test_toggle_status = TestViewSet.as_view({
#     "patch": "toggle_status",
# })

# result_list = LabTestResultViewSet.as_view({
#     "get": "list",
#     "post": "create",
# })
# result_detail = LabTestResultViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy",
# })
# results_by_pres = LabTestResultViewSet.as_view({
#     "get": "get_results_by_prescription",
# })

# billing_list = LabBillingViewSet.as_view({
#     "get": "list",
#     "post": "create",
# })
# billing_detail = LabBillingViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy",
# })
# bills_by_pres = LabBillingViewSet.as_view({
#     "get": "get_bills_by_prescription",
# })

# urlpatterns = [
#     # Categories
#     path("categories/", category_list, name="category-list"),
#     path("categories/<int:pk>/", category_detail, name="category-detail"),

#     # Tests
#     path("tests/", test_list, name="test-list"),
#     path("tests/<int:pk>/", test_detail, name="test-detail"),
#     path("tests/by-category/<int:cat_id>/", tests_by_category, name="tests-by-category"),

#     # Lab Results
#     path("results/", result_list, name="result-list"),
#     path("results/<int:pk>/", result_detail, name="result-detail"),
#     path("results/by-prescription/<int:pres_id>/", results_by_pres, name="results-by-pres"),

#     # Lab Billing
#     path("billings/", billing_list, name="billing-list"),
#     path("billings/<int:pk>/", billing_detail, name="billing-detail"),
#     path("billings/by-prescription/<int:pres_id>/", bills_by_pres, name="bills-by-pres"),
# ]
# # labtech_backend_app/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CategoryViewSet, TestViewSet, LabTestResultViewSet, LabBillingViewSet

# # Create a router and register our viewsets
# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'tests', TestViewSet, basename='test')
# router.register(r'lab-results', LabTestResultViewSet, basename='labresult')
# router.register(r'lab-billing', LabBillingViewSet, basename='labbilling')

# # The API URLs are now determined automatically by the router
# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TestViewSet, PrescriptionViewSet, 
    LabTestResultViewSet, LabBillingViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')  # NEW
router.register(r'lab-results', LabTestResultViewSet, basename='labresult')
router.register(r'lab-billing', LabBillingViewSet, basename='labbilling')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]