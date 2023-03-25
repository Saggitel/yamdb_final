from django.core.mail import send_mail


def send_code(recipient, code):
    subject = 'Регистрация на Yamdb'
    message = f'Ваш код для регистрации {code}'
    send_mail(
        subject,
        message,
        'admin@yambd.com',
        [recipient, ],
        fail_silently=False,
    )
