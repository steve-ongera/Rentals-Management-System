from django.shortcuts import render
from django.db.models import Avg
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from datetime import datetime
from django.urls import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect , get_object_or_404
from django.db.models import Count, Sum
from decimal import Decimal  # Import Decimal
from django.core.exceptions import MultipleObjectsReturned

import csv
###############
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
#from django.utils.encoding import force_bytes, force_text
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
###########################
import calendar
from .utils import generate_receipt
from django.http import FileResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# views.py
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from .models import Tenant, Payment
from django.template.loader import get_template
from django.http import HttpResponseNotAllowed


from django.shortcuts import render
from .models import Tenant, Payment
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from io import BytesIO
from .utils import generate_tenant_pdf, create_pdf_response


from django.http import JsonResponse
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
from django.db.models import Exists, OuterRef
from django.db.models import OuterRef, Exists, Subquery
from django.utils import timezone
import calendar

def download_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    tenant_name = f"{payment.tenant.first_name}_{payment.tenant.last_name}".replace(' ', '_')  # Adjust as per your naming convention
    pdf = generate_receipt(payment)
    return FileResponse(pdf, as_attachment=True, filename=f'receipt_{tenant_name}_932bbk&{payment_id}34210b7.pdf')


def is_admin_or_developer(user):
    return user.profile.user_type in ['admin', 'developer']

@login_required
@user_passes_test(is_admin_or_developer)

def admin_dashboard(request):
    # Count number of tenants
    num_workers = Worker.objects.count()
    num_non_workers = NonStaff.objects.count()
    num_tenants = Tenant.objects.count()

    # Retrieve all distinct years from the Payment_Year model
    years = Payment_Year.objects.all()

    # Dictionary to store payment data for each year
    payments_by_year = {}

    # Loop through each year and get payment data for that year
    for year in years:
        payments_by_month = Payment.objects.filter(year=year).values('month__name').annotate(total_payments=Count('id'), total_amount=Sum('amount'))
        payments_dict = {item['month__name']: item for item in payments_by_month}

        # Prepare data for chart (labels and data)
        labels = list(calendar.month_name)[1:]  # Exclude the empty first element
        total_payments_data = []
        total_amount_data = []

        for month in labels:
            if month in payments_dict:
                total_payments_data.append(payments_dict[month]['total_payments'])
                total_amount_data.append(float(payments_dict[month]['total_amount']))
            else:
                total_payments_data.append(0)
                total_amount_data.append(0.0)

        payments_by_year[year.name] = {
            'labels': labels,
            'total_payments_data': total_payments_data,
            'total_amount_data': total_amount_data,
        }

    # Calculate total sum of all payments
    total_sum = Payment.objects.aggregate(total_sum=Sum('amount'))['total_sum'] or 0.0

    context = {
        'num_tenants': num_tenants,
        'payments_by_year': payments_by_year,
        'total_sum': float(total_sum),  # Convert to float for consistency
        'num_workers': num_workers,  # Add number of workers to context
        'num_non_workers': num_non_workers,  # Add number of workers to context
        'years': years  # Add the distinct years to context
    }
    return render(request, 'admin_dashboard.html', context)





def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ' You have been logged in successfully.')
            return redirect('home')  # Replace 'dashboard' with your desired URL name
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ' Username & Password did not match. Try again.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    


    
    
def custom_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            identification_number = form.cleaned_data.get('identification_number')
            password = form.cleaned_data.get('password1')

            # Get the CompanyStaff instance
            staff = tenants_database.objects.get(username=username, identification_number=identification_number)

            # Create a new user
            if User.objects.filter(username=username):
                messages.warning(request,"The Username with that ID No already exist!")
            else:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user, user_type='guest')
                user.email = staff.email
                user.first_name = staff.first_name
                user.last_name = staff.last_name
                # Save other fields as needed

                user.save()
                login(request, user)
                messages.success(request, 'You account has been created successfully.')
                return redirect('home')
           
        
           
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'home.html') 


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('home'))



@login_required
@user_passes_test(lambda u: u.profile.user_type == 'guest')

def dashboard(request):
    tenant = Tenant.objects.filter(user_name=request.user.username).first()

    if not tenant:
        return render(request, 'error_404.html', {'user': request.user})

    payments = Payment.objects.filter(tenant=tenant)
    months = Month.objects.filter(payment__in=payments).distinct()
    month_payments_map = {}

    # Fetch relocation requests
    relocation_requests = RelocationRequest.objects.filter(tenant=tenant).order_by('-request_date')

    # Fetch leave notices
    leave_notices = LeaveNotice.objects.filter(tenant=tenant).order_by('-notice_date')

    for month in months:
        month_payments_map[month] = payments.filter(month=month)
    
    context = {
        'tenant': tenant,
        'month_payments_map': month_payments_map,
        'relocation_requests': relocation_requests,
        'leave_notices': leave_notices,
    }
    return render(request, 'dashboard.html', context)





def is_admin_or_developer(user):
    return user.profile.user_type in ['admin', 'developer']

@login_required
@user_passes_test(is_admin_or_developer)



def tenant_payment_status(request):
    tenants = Tenant.objects.all()
    months = Month.objects.all().order_by('start_date')
    
    payment_data = {}
    for tenant in tenants:
        payment_data[tenant] = {}
        for month in months:
            # Adjust this logic based on how you're tracking payments
            payment = Payment.objects.filter(tenant=tenant, month=month).exists()
            payment_data[tenant][month] = payment

    context = {
        'tenants': tenants,
        'months': months,
        'payment_data': payment_data,
    }
    return render(request, 'payment_record.html', context)




@login_required
@user_passes_test(is_admin_or_developer)


def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment added successfully.')
            return redirect('payment_status')
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form})



@login_required
@user_passes_test(is_admin_or_developer)


def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully.')
            return redirect('tenant_payment_status')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'edit_payment.html', {'form': form, 'payment': payment})



@login_required
@user_passes_test(is_admin_or_developer)

def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment deleted successfully.')
        return redirect('tenant_payment_status')
    return render(request, 'delete_payment.html', {'payment': payment})



def tenant_payment_history(request):
    return render(request, 'tenant_payment_history.html')


@login_required
@user_passes_test(is_admin_or_developer)

def tenant_list(request):
    tenants = Tenant.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, 'tenant_list.html', context)



@login_required
@user_passes_test(is_admin_or_developer)

def tenant_detail(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    payments = Payment.objects.filter(tenant=tenant)
    
    context = {
        'tenant': tenant,
        'payments': payments,
    }
    return render(request, 'tenant_detail.html', context)




@login_required
@user_passes_test(is_admin_or_developer)

def tenant_update(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success( request, 'Tenant data succesfully updated !')
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    context = {
        'form': form,
        'tenant': tenant
    }
    return render(request, 'tenant_update.html', context)



@login_required
@user_passes_test(is_admin_or_developer)

def tenant_delete(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        tenant.delete()
        messages.warning(request , 'Tenant data succesfully deleted')
        return redirect('tenant_list')
    context = {
        'tenant': tenant
    }
    return render(request, 'tenant_delete.html', context)

@login_required
def maintenance_request_create(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.tenant = tenant
            request_obj.save()
            messages.success(request, 'Maintenance request submitted successfully.')
            #return redirect('tenant_detail', tenant_id=tenant.id)
            return redirect('maintenance_request_list')
    else:
        form = MaintenanceRequestForm()
    
    context = {
        'form': form,
        'tenant': tenant,
    }
    return render(request, 'maintenance_request_create.html', context)



def maintenance_request_list(request):
    if request.user.profile.user_type == 'admin':
        requests = MaintenanceRequest.objects.all()
    else:
        # Get the current logged-in user's tenant instance
       current_tenant = Tenant.objects.get(user_name=request.user.username)
       requests = MaintenanceRequest.objects.filter(tenant=current_tenant)
    
    context = {
        'requests': requests,
    }
    return render(request, 'maintenance_request_list.html', context)


def respond_to_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.cleaned_data['response']
            maintenance_request.response = response  # Save response to model
            maintenance_request.status = 'responded'
            maintenance_request.save()
            messages.success(request, 'Response sent successfully.')
            return redirect('maintenance_request_list')
    else:
        form = ResponseForm()
    
    context = {
        'maintenance_request': maintenance_request,
        'form': form,
    }
    return render(request, 'respond_to_request.html', context)


@login_required
@user_passes_test(is_admin_or_developer)

def add_tenant(request):
    if request.method =='POST':
        form=TenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant Data successfully added to Tenants Database.')
            return redirect('tenant_list')
    else:
        form= TenantForm()
    return render(request, 'add_tenant.html', { 'form':form})




@login_required
@user_passes_test(is_admin_or_developer)

def add_tenant_databse(request):
    if request.method =='POST':
        form=tenants_databaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Information successfully added to Application Database.')
            return redirect('user_list')
    else:
        form= tenants_databaseForm()
    return render(request, 'add_tenant_databse.html', { 'form':form})



@login_required
@user_passes_test(is_admin_or_developer)

def user_list(request):
    tenants = tenants_database.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, 'user_list.html', context)




@login_required
@user_passes_test(is_admin_or_developer)

def add_house(request):
    if request.method =='POST':
        form=HouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'House  successfully created.')
            return redirect('house_list')
    else:
        form= HouseForm()
    return render(request, 'house.html', { 'form':form})



@login_required
@user_passes_test(is_admin_or_developer)

def house_list(request):
    tenants = House.objects.all()
    context = {
        'tenants': tenants
    }
    return render(request, 'house_list.html', context)




@login_required
@user_passes_test(is_admin_or_developer)




def search_tenant(request):
    if request.method == 'POST':
        identification_number = request.POST.get('identification_number', '')
        try:
            tenant = Tenant.objects.get(identification_number=identification_number)
            payments = Payment.objects.filter(tenant=tenant)
            
            # Check if download is requested
            if 'download' in request.POST:
                pdf_content = generate_tenant_pdf(tenant, payments)
                return create_pdf_response(pdf_content, f"tenant_{identification_number}_payments.pdf")
            
        except Tenant.DoesNotExist:
            tenant = None
            payments = None
        
        return render(request, 'search_tenant.html', {'tenant': tenant, 'payments': payments, 'search_performed': True})
    else:
        return render(request, 'search_tenant.html', {'search_performed': False})


def search_payment(request):
    tenant = None
    payments = []
    if request.method == 'POST':
        mpesa_code = request.POST.get('mpesa_code', '')
        try:
            payment = Payment.objects.get(mpesa_code=mpesa_code)
            tenant = payment.tenant
            payments = Payment.objects.filter(tenant=tenant)
        except Payment.DoesNotExist:
            tenant = None
        
    return render(request, 'search_payment.html', {'tenant': tenant, 'payments': payments})



Account = get_user_model()


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            # Generate reset password token and send email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            }
            
            # Render both HTML and plain text versions of the email
            html_message = render_to_string('reset_password_email.html', context)
            plain_message = strip_tags(html_message)
            
            to_email = email
            
            # Use EmailMultiAlternatives for sending both HTML and plain text
            email = EmailMultiAlternatives(
                mail_subject,
                plain_message,
                'noreply@yourdomain.com',
                [to_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')







def reset_password(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful. You can now login with your new password.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_password', uidb64=uidb64, token=token)
        return render(request, 'reset_password.html')
    else:
        messages.error(request, 'Invalid reset link. Please try again.')
        return redirect('login')


def homepage(request):
    return render(request, 'homepage.html')

def process_query(request):
    query = request.POST.get('query', '')
    response = None

    if query:
        try:
            # Attempt to find the most appropriate answer
            qna_responses = QnAResponse.objects.filter(question__icontains=query)
            
            if qna_responses.exists():
                # If exact match found, prioritize it
                qna_response_exact = qna_responses.filter(question__iexact=query).first()
                if qna_response_exact:
                    response = qna_response_exact.response
                else:
                    # If no exact match, take the first one found
                    response = qna_responses.first().response
            else:
                response = "Sorry, I don't have an answer for that question."
        
        except QnAResponse.DoesNotExist:
            response = "Sorry, I don't have an answer for that question."
        except MultipleObjectsReturned:
            # Handle multiple matching objects (if necessary)
            response = "Multiple answers found. Please refine your question."

    return render(request, 'homepage.html', {'query': query, 'response': response})

def get_response(user_query):
    try:
        # Search for the question in the database (exact match)
        qna_response = QnAResponse.objects.get(question__iexact=user_query)
        return qna_response.response
    except QnAResponse.DoesNotExist:
        return "I'm sorry, I don't have a response for that question."
    except MultipleObjectsReturned:
        # Handle multiple matching objects (if necessary)
        return "Multiple answers found. Please refine your question."
    


def worker_list(request):
    workers = Worker.objects.all()
    return render(request, 'worker_list.html', {'workers': workers})

def worker_detail(request, id):
    worker = get_object_or_404(Worker, id=id)
    return render(request, 'worker_detail.html', {'worker': worker})


def update_worker(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    if request.method == 'POST':
        form = WorkerForm(request.POST, request.FILES, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('worker_list')  # Redirect to the workers list or another page after saving
    else:
        form = WorkerForm(instance=worker)
    
    return render(request, 'update_worker.html', {'form': form, 'worker': worker})


def delete_worker(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    
    if request.method == 'POST':
        worker.delete()
        messages.success(request, "Worker deleted successfully.")
        return redirect('worker_list')  # Adjust URL name as needed
    
    return render(request, 'delete_worker.html', {'worker': worker})


def add_worker(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('worker_list')  # Redirect to the list view or any other page
    else:
        form = WorkerForm()

    return render(request, 'add_worker.html', {'form': form, 'page_title': 'Add New Worker'})


def non_staff_list(request):
    non_staff_members = NonStaff.objects.all()
    return render(request, 'non_staff_list.html', {'non_staff_members': non_staff_members})

def add_non_staff(request):
    if request.method == 'POST':
        form = NonStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('non_staff_list')
    else:
        form = NonStaffForm()
    return render(request, 'add_non_staff.html', {'form': form})

def non_staff_detail(request, pk):
    non_staff_member = get_object_or_404(NonStaff, pk=pk)
    return render(request, 'non_staff_detail.html', {'non_staff_member': non_staff_member})



@login_required
def tenant_payment(request):
    try:
        tenant = Tenant.objects.get(user_name=request.user.username)
    except Tenant.DoesNotExist:
        messages.error(request, "Tenant profile not found.")
        return redirect('some_error_page')  # Replace with appropriate error page

    if request.method == 'POST':
        form = UserPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = tenant
            
            # Check if a payment for this month already exists
            if Payment.objects.filter(tenant=tenant, month=payment.month).exists():
                messages.error(request, "A payment for this month already exists.")
                return redirect('tenant_payment')
            
            payment.save()
            messages.success(request, "Payment submitted successfully!")
            return redirect('payment_confirmation', payment_id=payment.id)
    else:
        form = UserPaymentForm()
    
    # Get all months that haven't been paid for yet
    paid_months = Payment.objects.filter(tenant=tenant).values_list('month', flat=True)
    available_months = Month.objects.exclude(id__in=paid_months)
    
    form.fields['month'].queryset = available_months

    context = {
        'form': form,
        'tenant': tenant,
    }
    return render(request, 'tenant_payment.html', context)


@login_required
def payment_confirmation(request, payment_id):
    # Retrieve the payment object, ensuring it belongs to the logged-in user
    payment = get_object_or_404(Payment, id=payment_id, tenant__user_name=request.user.username)
    
    context = {
        'payment': payment,
        'tenant': payment.tenant,
        'month': payment.month,
    }
    
    return render(request, 'payment_confirmation.html', context)





@login_required
def relocation_request(request):
    if request.method == 'POST':
        form = RelocationRequestForm(request.POST)
        if form.is_valid():
            relocation_request = form.save(commit=False)
            relocation_request.tenant = request.user.tenant
            relocation_request.current_house = request.user.tenant.house
            relocation_request.save()
            messages.success(request, 'Relocation request submitted successfully.')
            return redirect('dashboard')
    else:
        form = RelocationRequestForm()
    return render(request, 'relocation_request.html', {'form': form})



@login_required
def apply_leave_notice(request):
    if request.method == 'POST':
        form = LeaveNoticeForm(request.POST)
        if form.is_valid():
            leave_notice = form.save(commit=False)
            tenant = Tenant.objects.get(user_name=request.user.username)
            leave_notice.tenant = tenant
            leave_notice.house = tenant.house
            leave_notice.save()
            messages.success(request, "Leave notice submitted successfully. Your request will be reviewed.")
            return redirect('home')  # Redirect to a relevant page
    else:
        form = LeaveNoticeForm()

    return render(request, 'apply_leave_notice.html', {'form': form})

def list_leave_notices(request):
    leave_notices = LeaveNotice.objects.all()
    return render(request, 'list_leave_notices.html', {'leave_notices': leave_notices})


def respond_leave_notice(request, notice_id):
    leave_notice = get_object_or_404(LeaveNotice, id=notice_id)
    
    if request.method == 'POST':
        form = LeaveNoticeForm(request.POST, instance=leave_notice)
        if form.is_valid():
            leave_notice = form.save(commit=False)
            leave_notice.status = 'approved'  # Change status to approved
            leave_notice.save()
            messages.success(request, "Response saved successfully and status updated to 'completed'.")
            return redirect('list_leave_notices')
    else:
        form = LeaveNoticeForm(instance=leave_notice)
    
    return render(request, 'respond_leave_notice.html', {'form': form, 'leave_notice': leave_notice})



def tenant_leave_notices(request):
    tenant = Tenant.objects.get(user_name=request.user.username)
    leave_notices = LeaveNotice.objects.filter(tenant=tenant)
    return render(request, 'tenant_leave_notices.html', {'leave_notices': leave_notices})


@login_required
def delete_leave_notice(request, notice_id):
    leave_notice = get_object_or_404(LeaveNotice, id=notice_id)

    # Ensure the leave notice belongs to the logged-in tenant
    if leave_notice.tenant.user_name != request.user.username:
        messages.error(request, "You do not have permission to delete this leave notice.")
        return redirect('tenant_leave_notices')

    if request.method == 'POST':
        leave_notice.delete()
        messages.success(request, "Leave notice deleted successfully.")
        return redirect('tenant_leave_notices')

    return render(request, 'confirm_delete_leave_notice.html', {'leave_notice': leave_notice})


def list_houses(request):
    # Subquery to get the planned leave date for each house if there's an active leave notice
    leave_notice_subquery = LeaveNotice.objects.filter(
        house=OuterRef('pk'),
        planned_leave_date__gte=timezone.now().date(),
        status='approved'
    ).values('planned_leave_date')[:1]

    # Annotate houses with the leave notice status and planned leave date
    houses = House.objects.annotate(
        has_leave_notice=Exists(leave_notice_subquery),
        leave_date=Subquery(leave_notice_subquery)
    )
    
    return render(request, 'list_houses.html', {'houses': houses})

def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    return render(request, 'house_detail.html', {'house': house})


def book_house(request, house_id):
    house = get_object_or_404(House, id=house_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check if the house is vacant before proceeding
            if not house.is_vacant:
                form.add_error(None, "The selected house is not available for booking.")
                return render(request, 'book_house.html', {'form': form, 'house': house})

            # Create and save the booking instance
            booking = form.save(commit=False)
            booking.house = house
            booking.deposit_amount = house.booking_amount  # Set deposit amount from house
            booking.save()

            # Update house status
            house.is_vacant = False
            house.is_booked = True
            house.save()

            return redirect('booking_success')  # Redirect to a success page or home
    else:
        # Initialize form with the house information
        form = BookingForm(initial={'house': house})

    return render(request, 'book_house.html', {'form': form, 'house': house})




def booking_success(request):
    return render(request, 'booking_success.html')


def booked_houses_list(request):
    bookings = Booking.objects.all()    
    return render(request, 'booked_houses_list.html', {'bookings': bookings})