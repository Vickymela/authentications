import random
from django.contrib.auth.models import User
from .models import *


def generate_otp(user):
    print('hit otp generation')
    
    # Generate random OTP
    rand = random.randint(1000, 9999)

    # Check if an OTP already exists for this user
    otp, created = Otp.objects.get_or_create(user=user, defaults={'code': rand, 'status': False})

    if not created:
        # If OTP exists, update the code and reset status
        otp.code = rand
        otp.status = False
        otp.save()

    return rand

def Verify_otp(user, code):
    """
    Verifies the OTP for a given user.
    user: User instance
    code: int or str
    Returns True if OTP matches, False otherwise.
    """

    print('hit otp verification')

    try:
        otp_record = Otp.objects.get(user=user)
    except Otp.DoesNotExist:
        # No OTP exists for this user
        return False

    # Check if the code matches
    if otp_record.code == int(code):  # make sure code types match
        # Optionally mark OTP as used
        otp_record.status = True
        otp_record.save()
        return True

    return False
