from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from submissions.models import Submission
from .models import ProducerProfile


def producer_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_producer():
            messages.error(request, 'Access denied.')
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@login_required
@producer_required
def producer_dashboard(request):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    genres = profile.genres.all()
    pending = Submission.objects.filter(
        genre__in=genres, payment_completed=True, status=Submission.STATUS_PENDING
    ).select_related('artist', 'genre')
    under_review = Submission.objects.filter(
        genre__in=genres, reviewed_by=request.user, status=Submission.STATUS_UNDER_REVIEW
    ).select_related('artist', 'genre')
    return render(request, 'producers/dashboard.html', {
        'pending': pending,
        'under_review': under_review,
        'profile': profile,
    })


@login_required
@producer_required
def review_submission(request, pk):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    submission = get_object_or_404(Submission, pk=pk, genre__in=profile.genres.all())
    if request.method == 'POST':
        decision = request.POST.get('decision')
        notes = request.POST.get('notes', '')
        if decision in [Submission.STATUS_SELECTED, Submission.STATUS_NOT_SELECTED, Submission.STATUS_UNDER_REVIEW]:
            submission.status = decision
            submission.producer_notes = notes
            submission.reviewed_by = request.user
            submission.reviewed_at = timezone.now()
            submission.save()
            messages.success(request, f'Submission marked as {submission.get_status_display()}.')
            return redirect('producers:dashboard')
    if submission.status == Submission.STATUS_PENDING:
        submission.status = Submission.STATUS_UNDER_REVIEW
        submission.reviewed_by = request.user
        submission.save()
    return render(request, 'producers/review.html', {'submission': submission})


@login_required
@producer_required
def reviewed_submissions(request):
    profile = get_object_or_404(ProducerProfile, user=request.user)
    reviewed = Submission.objects.filter(
        genre__in=profile.genres.all(),
        reviewed_by=request.user,
        status__in=[Submission.STATUS_SELECTED, Submission.STATUS_NOT_SELECTED]
    ).select_related('artist', 'genre').order_by('-reviewed_at')
    return render(request, 'producers/reviewed.html', {'reviewed': reviewed})
