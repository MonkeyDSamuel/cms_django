# Lab test methods to add to LabPrescriptionSerializer

def get_test_name(self, obj):
    return obj.lab_test.test_name if obj.lab_test else None

def get_test_type(self, obj):
    return obj.lab_test.test_type if obj.lab_test else None

def get_test_instructions(self, obj):
    return obj.lab_test.test_instructions if obj.lab_test else None

def get_test_fasting_required(self, obj):
    return obj.lab_test.test_fasting_required if obj.lab_test else False
