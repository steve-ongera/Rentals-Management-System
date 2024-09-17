from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
#('February', 'February'),

class Month(models.Model):
    TERM_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    name = models.CharField(max_length=10, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('guest', 'Guest'),
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    


    
class Payment_Year(models.Model):
    name = models.CharField(max_length=100)
    month = models.ManyToManyField(Month )

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=100)
    house_number = models.PositiveIntegerField()  # To store the house number
    is_vacant = models.BooleanField(default=True)  # To indicate whether the house is vacant or not
    description = models.TextField(blank=True, null=True)  # To store a description of the house
    rent_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Rent fee for the house
    image1 = models.ImageField(upload_to='houses/images/', blank=True, null=True)  # First image
    image2 = models.ImageField(upload_to='houses/images/', blank=True, null=True)  # Second image
    image3 = models.ImageField(upload_to='houses/images/', blank=True, null=True)  # Third im
    is_booked = models.BooleanField(default=False) 
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Amount for booking

    class Meta:
        unique_together = ('name', 'house_number')  # Ensuring uniqueness

    def __str__(self):
        return f"{self.name} {self.house_number}"



class Tenant(models.Model):
  
    user_name = models.CharField(max_length=100)
    identification_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    avatar = models.ImageField(upload_to='media', default='media/avatar.svg')
    house = models.ForeignKey(House,  on_delete=models.CASCADE)
    tap_no = models.CharField(max_length=100 , null=True, blank=True)
   
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}~{self.identification_number}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_tenant = Tenant.objects.get(pk=self.pk)
            if old_tenant.house != self.house:
                # If house has changed, update the old house
                old_house = old_tenant.house
                old_house.is_vacant = True
                old_house.save()
                
        super().save(*args, **kwargs)
        
        # Update the new house
        if self.house:
            self.house.is_vacant = False
            self.house.save()



class tenants_database(models.Model):
    username = models.CharField(max_length=100 )
    identification_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar.svg')
  
    

    def __str__(self):
        return f"{self.username} ~ {self.first_name} {self.last_name} - {self.identification_number}"
    


class MonthlySignOff(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    signed_off = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('tenant', 'month')

    def __str__(self):
        return f"{self.tenant.first_name} {self.tenant.last_name} - {self.month.name}"
    

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_code=models.CharField(max_length=100)
    date_paid = models.DateField()

    class Meta:
        unique_together = ('tenant', 'month')

    def __str__(self):
        return f"{self.tenant} - {self.month} - {self.amount}-{self.date_paid}"
    





class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    response = models.TextField(blank=True)
    
    def __str__(self):
        return f"Request from {self.tenant.first_name} {self.tenant.last_name} - {self.date_created}"


class QnAResponse(models.Model):
    question = models.CharField(max_length=255)
    response = models.TextField()

    def __str__(self):
        return self.question
    

class Worker(models.Model):
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    role = models.CharField(max_length=100)
    dob= models.DateField( blank=True , null=True)
    photo = models.ImageField(upload_to='workers/photos/', default='workers/photos/avatar.svg')
    passport_photo = models.ImageField(upload_to='workers/passport_photos/', default='workers/passport_photos/Kenya-ID.jpg')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
    


class NonStaff(models.Model):
    id_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
    


class RelocationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    current_house = models.ForeignKey(House, related_name='current_relocations', on_delete=models.CASCADE)
    desired_house = models.ForeignKey(House, related_name='desired_relocations', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    decision_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Relocation request by {self.tenant} - {self.status}"
    

class LeaveNotice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    planned_leave_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notice_date = models.DateTimeField(auto_now_add=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Leave notice by {self.tenant} - {self.status}"

    def clean(self):
        # Ensure the planned leave date is at least 30 days in the future
        if self.planned_leave_date:
            min_notice_date = timezone.now().date() + timezone.timedelta(days=30)
            if self.planned_leave_date < min_notice_date:
                raise ValidationError("Planned leave date must be at least 30 days in the future.")



class Booking(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    identification_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure the deposit amount is not less than 4500
        if self.deposit_amount is None or self.deposit_amount < 100:
            raise ValidationError("Deposit amount must be at least 100.")

        # Check if the house is vacant
        if self.house is None or not self.house.is_vacant:
            raise ValidationError("The house is not available for booking.")

        # Ensure the deposit amount matches the booking amount of the house
        if self.house.booking_amount is None or self.deposit_amount != self.house.booking_amount:
            raise ValidationError("Deposit amount must be equal to the booking amount of the house.")

    def save(self, *args, **kwargs):
        # Validate deposit amount before saving
        self.clean()
        super().save(*args, **kwargs)

        # Update house status to occupied
        if self.house:
            self.house.is_vacant = False
            self.house.is_booked = True
            self.house.save()

    def __str__(self):
        return f"Booking by {self.name} for {self.house.name}"