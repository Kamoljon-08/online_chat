from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser

class UserModel (AbstractUser):
    bio = models.CharField(name='bio', max_length=80)
    id = models.AutoField(name='id', primary_key=True)
    block = models.BooleanField(name='block', default=False)
    last_name = models.CharField(name='last_name', max_length=70, blank=False, null=False)
    first_name = models.CharField(name='first_name', max_length=70, blank=False, null=False)
    created_at = models.DateTimeField(name='created_at', auto_now_add=True)
    username = models.CharField(name='username', max_length=70, blank=True, null=True, unique=True)
    phone = models.CharField(name='phone', max_length=30, blank=False, null=False)
    images = models.ImageField(upload_to='uploads/avatar', blank=False, null=False)
    image_thumbnail = ImageSpecField(
        format='JPEG',
        source='images',
        options={'quality': 60},
        processors=[ResizeToFill(500, 500)],
    )

    otp = models.CharField(max_length=6, null=True, blank=True)

    def str(self) -> str:
        return str(self.id)

# from django.dispatch import receiver
# from django.urls import reverse
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.core.mail import send_mail

# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title
#         "Password Reset for {title}".format(title="Some website title"),

#         #message
#         email_plaintext_message,

#         # from
#         'noreply@somehost.local',
        
#         # to
#         [reset_password_token.user.email]
#     )