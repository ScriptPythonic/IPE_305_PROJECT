import requests

def send_welcome_email(name, email):
    service_id = 'service_ju4lwek'
    template_id = 'template_befvdg8'
    user_id = 'wfx417tfWrYqMAvgF'
    
    template_params = {
        'to_name': name,
        'to_email': email,
    }

    response = requests.post(
        f'https://api.emailjs.com/api/v1.0/email/send',
        json={
            'service_id': service_id,
            'template_id': template_id,
            'user_id': user_id,
            'template_params': template_params,
        }
    )

    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print('Failed to send email:', response.text)
