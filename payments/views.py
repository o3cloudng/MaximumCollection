from django.shortcuts import render, redirect
from .models import Payment, UserWallet
from django.conf import settings

def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST['amount']) * 100
        email = request.POST['email']
        referenceid = request.POST['referenceid']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, user=request.user, referenceid=referenceid)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount,
        }
        return render(request, 'payments/make_payment.html', context)

    return render(request, 'payments/payment.html')


def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        user_wallet = UserWallet.objects.get(user=request.user)
        user_wallet.balance += payment.amount
        user_wallet.save()
        print(request.user.username, " funded wallet successfully")
        return render(request, "success.html")
    return render(request, "success.html")

