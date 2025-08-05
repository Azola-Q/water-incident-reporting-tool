from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.http import HttpResponse

import ssl
ssl._create_default_https_context = ssl._create_unverified_context  # For local email testing

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

from .models import User, Issue
from .forms import UserRegisterForm, UserUpdateForm, IssueForm, PasswordResetRequestForm, PasswordResetForm


def login_view(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        # Authenticate using custom backend that expects id_number
        user = authenticate(request, id_number=id_number, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            return redirect('home')
        else:
            messages.error(request, 'Invalid ID number or password.')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Optional: sync username to id_number if you use username elsewhere
            user.username = user.id_number
            user.save()  # Password is hashed inside form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home_view(request):
    if request.user.is_staff:
        return redirect('/admin/')

    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            messages.success(request, 'Your complaint has been received. Our team will process it shortly.')
            return redirect('status')
    else:
        form = IssueForm()

    return render(request, 'home.html', {'form': form})


@login_required
def edit_details_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details updated successfully.')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'edit_details.html', {'form': form})


@login_required
def status_view(request):
    export = request.GET.get('export', '').strip()
    issue_type = request.GET.get('issue_type', '').strip()
    status_filter = request.GET.get('status', '').strip()

    issues = Issue.objects.filter(user=request.user)
    if issue_type:
        issues = issues.filter(issue_type=issue_type)
    if status_filter:
        issues = issues.filter(status=status_filter)

    if export == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="complaints.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4,
                                rightMargin=1.2 * cm, leftMargin=1.2 * cm,
                                topMargin=1.5 * cm, bottomMargin=1.5 * cm)
        styles = getSampleStyleSheet()
        wrap_style = ParagraphStyle(name='WrapStyle', fontSize=8, leading=10)
        elements = []

        elements.append(Paragraph("Water Incident Reports", styles['Title']))
        elements.append(Spacer(1, 12))

        data = [['Issue Type', 'Description', 'Status', 'Created At', 'Latitude', 'Longitude']]
        col_widths = [3.2 * cm, 6.5 * cm, 2.3 * cm, 3.2 * cm, 1.7 * cm, 1.7 * cm]

        for issue in issues:
            data.append([
                issue.get_issue_type_display(),
                Paragraph(issue.description, wrap_style),
                issue.get_status_display(),
                issue.created_at.strftime('%Y-%m-%d %H:%M'),
                str(issue.latitude) if issue.latitude else '-',
                str(issue.longitude) if issue.longitude else '-',
            ])

        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    return render(request, 'status.html', {'issues': issues})


def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            try:
                user = User.objects.get(id_number=id_number)
                # Generate a separate token and save it to a dedicated field (you'll need to add this field to User model)
                token = get_random_string(32)
                user.password_reset_token = token
                user.save()

                reset_url = request.build_absolute_uri(reverse('reset_password', kwargs={'token': token}))
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {reset_url}',
                    from_email='noreply@waterincidenttool.com',
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                messages.success(request, 'Password reset link sent to your email.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this ID number.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'forgot_password.html', {'form': form})


def reset_password_view(request, token):
    try:
        user = User.objects.get(password_reset_token=token)
    except User.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('forgot_password')

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.password_reset_token = ''  # Clear token
            user.save()
            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
