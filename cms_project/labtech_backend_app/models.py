from django.db import models
from django.utils import timezone
from doctor_backend_app.models import LabPrescription  # ADD THIS IMPORT


# ----------------------------
# Category Table
# ----------------------------
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


# ----------------------------
# Common Test Table
# ----------------------------
class Test(models.Model):
    id = models.AutoField(primary_key=True)
    test_id = models.CharField(max_length=10, unique=True, editable=False)  # TS001, TS002...
    test_name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tests")
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.test_id:
            last_test = Test.objects.order_by("-id").first()
            if last_test:
                last_num = int(last_test.test_id.replace("TS", ""))
                new_num = last_num + 1
            else:
                new_num = 1
            self.test_id = f"TS{new_num:03d}"  # Format like TS001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.test_id} - {self.test_name}"



# ----------------------------
# Prescription Table (UPDATED)
# ----------------------------
class Prescription(models.Model):
    pres_id = models.AutoField(primary_key=True)
    lab_prescription = models.OneToOneField(  # ADD THIS FIELD
        LabPrescription, 
        on_delete=models.CASCADE, 
        related_name="lab_prescription",
        null=True,
        blank=True
    )
    patient_name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=20)
    doctor_name = models.CharField(max_length=100)
    prescription_date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PR{self.pres_id:04d} - {self.patient_name}"  # FIXED: Added self.

    def save(self, *args, **kwargs):
        # Auto-fill from lab_prescription if available
        if self.lab_prescription and not self.patient_name:
            consultation = self.lab_prescription.consultation
            appointment = consultation.AppointmentId
            self.patient_name = f"{appointment.PatientId.FirstName} {appointment.PatientId.LastName}"
            self.patient_id = appointment.PatientId.PatientId
            self.doctor_name = f"{appointment.DoctorId.FirstName} {appointment.DoctorId.LastName}"
        super().save(*args, **kwargs)

# ----------------------------
# Lab Test Result Table (UPDATED with ForeignKey to Prescription)
# ----------------------------
class LabTestResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="results")
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="lab_results", null=True, blank=True)  # NEW
    status = models.CharField(
        max_length=50, 
        choices=[
            ("Pending", "Pending"), 
            ("Completed", "Completed"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected")
        ],
        default="Pending"
    )
    result_value = models.TextField(blank=True, null=True)  # NEW
    normal_range = models.TextField(blank=True, null=True)  # NEW
    unit = models.CharField(max_length=50, blank=True, null=True)  # NEW
    remarks = models.TextField(blank=True, null=True)  # NEW
    result_date = models.DateField(default=timezone.now)
    created_on = models.DateTimeField(default=timezone.now)  # NEW

    def __str__(self):
        return f"Result {self.result_id} - {self.test.test_name}"


# ----------------------------
# Lab Billing Table (UPDATED with ForeignKey to Prescription)
# ----------------------------
class LabBilling(models.Model):
    bill_id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="lab_bills", null=True, blank=True)  # NEW
    bill_number = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)  # NEW
    patient_name = models.CharField(max_length=100, null=True, blank=True)  # NEW
    patient_id = models.CharField(max_length=20, null=True, blank=True)  # NEW
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # NEW
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # NEW
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # NEW
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # UPDATED (was charge)
    payment_method = models.CharField(  # NEW
        max_length=20,
        choices=[
            ('Cash', 'Cash'),
            ('Card', 'Card'),
            ('UPI', 'UPI'),
            ('Insurance', 'Insurance')
        ],
        default='Cash'
    )
    status = models.CharField(  # NEW
        max_length=20,
        choices=[
            ('Generated', 'Generated'),
            ('Paid', 'Paid'),
            ('Pending', 'Pending'),
            ('Cancelled', 'Cancelled')
        ],
        default='Generated'
    )
    remarks = models.TextField(blank=True, null=True)  # NEW
    billing_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.bill_number:
            last_bill = LabBilling.objects.order_by("-bill_id").first()
            if last_bill:
                last_num = int(last_bill.bill_number.replace("BL", ""))
                new_num = last_num + 1
            else:
                new_num = 1
            self.bill_number = f"BL{new_num:04d}"  # Format like BL0001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.bill_number} - {self.total_amount}"


# ----------------------------
# Billing Item Table (NEW - for detailed billing)
# ----------------------------
class BillingItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    billing = models.ForeignKey(LabBilling, on_delete=models.CASCADE, related_name="items")
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=150)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    lab_result = models.ForeignKey(LabTestResult, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.test_name} - ₹{self.rate}"