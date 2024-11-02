from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
        }

class tenants_databaseForm(forms.ModelForm):
    class Meta:
        model = tenants_database
        fields = '__all__'  # You can specify fields explicitly if needed
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    identification_number = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        identification_number = cleaned_data.get('identification_number')

        if username and identification_number:
            try:
                staff = tenants_database.objects.get(username=username, identification_number=identification_number)
            except tenants_database.DoesNotExist:
                raise ValidationError('The provided username & ID dont match.')

        return cleaned_data


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'  # or specify fields you want to update




class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['description']


class ResponseForm(forms.Form):
    response = forms.CharField(label='Your Response', widget=forms.Textarea)


class TenatForm(ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
     
class TenatRegisterDatabaseForm(ModelForm):
    class Meta:
        model = tenants_database
        fields = '__all__'
     

class HouseForm(ModelForm):
    class Meta:
        model = House
        fields = '__all__'

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['id_number', 'first_name', 'last_name', 'email', 'phone', 'address', 'role', 'photo', 'passport_photo','gender','dob']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'passport_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import NonStaff

class NonStaffForm(forms.ModelForm):
    class Meta:
        model = NonStaff
        fields = '__all__'



class TenantPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
        }




class UserPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['year', 'month', 'amount', 'mpesa_code', 'date_paid']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Initialize month field with empty queryset
    #     self.fields['month'].queryset = Month.objects.none()
        
    #     # Get form data if it exists
    #     if 'data' in kwargs:
    #         try:
    #             year_id = kwargs['data'].get('year')
    #             if year_id:
    #                 year = Payment_Year.objects.get(id=year_id)
    #                 self.fields['month'].queryset = year.month.all()
    #         except (ValueError, Payment_Year.DoesNotExist):
    #             pass





class RelocationRequestForm(forms.ModelForm):
    class Meta:
        model = RelocationRequest
        fields = ['desired_house', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desired_house'].queryset = House.objects.exclude(id=self.instance.tenant.house.id)


class LeaveNoticeForm(forms.ModelForm):
    class Meta:
        model = LeaveNotice
        fields = ['planned_leave_date', 'reason']
        widgets = {
            'planned_leave_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_planned_leave_date(self):
        planned_leave_date = self.cleaned_data.get('planned_leave_date')
        if planned_leave_date:
            min_notice_date = timezone.now().date() + timezone.timedelta(days=30)
            if planned_leave_date < min_notice_date:
                raise forms.ValidationError("Planned leave date must be at least 30 days in the future.")
        return planned_leave_date
    

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['house', 'name', 'identification_number', 'phone', 'email','deposit_amount']
        widgets = {
            'house': forms.HiddenInput(),  # Hide the house field if using URL to pass house_id
        }

    def clean(self):
        cleaned_data = super().clean()
        house = cleaned_data.get('house')
        
        if house:
            # Check if the house is vacant before allowing booking
            if not house.is_vacant:
                raise forms.ValidationError("The selected house is not available for booking.")
            
        return cleaned_data