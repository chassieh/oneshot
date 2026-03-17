from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import SubmissionForm
from .models import Submission, Payment
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def submit_song(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.artist = request.user
            submission.save()
            return redirect('submissions:checkout', pk=submission.pk)
    else:
        form = SubmissionForm()
    return render(request, 'submissions/submit.html', {
        'form': form,
        'fee': settings.SUBMISSION_FEE,
    })


@login_required
def checkout(request, pk):
    submission = get_object_or_404(Submission, pk=pk, artist=request.user)
    if submission.payment_completed:
        return redirect('submissions:detail', pk=pk)
    return render(request, 'submissions/checkout.html', {
        'submission': submission,
        'fee': settings.SUBMISSION_FEE,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    })


@login_required
def stripe_payment(request, pk):
    submission = get_object_or_404(Submission, pk=pk, artist=request.user)
    if submission.payment_completed:
        return redirect('submissions:detail', pk=pk)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Shot at a Deal - {submission.song_title}'},
                    'unit_amount': int(settings.SUBMISSION_FEE * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/submissions/{pk}/stripe-success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(f'/submissions/{pk}/checkout/'),
            metadata={'submission_id': str(pk)},
        )
        return redirect(session.url, code=303)
    except Exception as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('submissions:checkout', pk=pk)


@login_required
def stripe_success(request, pk):
    submission = get_object_or_404(Submission, pk=pk, artist=request.user)
    session_id = request.GET.get('session_id')
    if session_id and not submission.payment_completed:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                submission.payment_completed = True
                submission.save()
                Payment.objects.get_or_create(
                    submission=submission,
                    defaults={
                        'user': request.user,
                        'amount': settings.SUBMISSION_FEE,
                        'method': Payment.METHOD_STRIPE,
                        'status': Payment.STATUS_COMPLETED,
                        'transaction_id': session.payment_intent,
                    }
                )
                messages.success(request, 'Payment successful! Your submission is now under review.')
        except Exception as e:
            messages.error(request, f'Could not verify payment: {str(e)}')
    return redirect('submissions:detail', pk=pk)


@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk, artist=request.user)
    return render(request, 'submissions/detail.html', {'submission': submission})


@login_required
def submission_list(request):
    submissions = Submission.objects.filter(artist=request.user).select_related('genre')
    return render(request, 'submissions/list.html', {'submissions': submissions})


@login_required
def paypal_success(request, pk):
    submission = get_object_or_404(Submission, pk=pk, artist=request.user)
    order_id = request.GET.get('order_id')
    if order_id and not submission.payment_completed:
        submission.payment_completed = True
        submission.save()
        Payment.objects.get_or_create(
            submission=submission,
            defaults={
                'user': request.user,
                'amount': settings.SUBMISSION_FEE,
                'method': Payment.METHOD_PAYPAL,
                'status': Payment.STATUS_COMPLETED,
                'transaction_id': order_id,
            }
        )
        messages.success(request, 'PayPal payment successful! Your submission is now under review.')
    return redirect('submissions:detail', pk=pk)



