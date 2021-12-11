from django.core.mail import send_mail
from seesky.passwords import EMAIL_ADRESS


class EmailHandler:
    def __init__(self):
        self.emali = EMAIL_ADRESS

    def validation(self, email, token, name, site_url):
        send_mail(
            'Potwierdzenie emaila',
            f'Witaj {name}.\nZapisałeś się na newsletter, aby potwierdzić swój email kliknij w poniższy link\n"'
            f'{site_url}/validate/{email}/{token}\n'
            f'Jeśli to nie Ty zapisałeś się na newsletter, zignoruj ten email\n'
            f'aby wypisać się z newslettera kliknij na poniższy link\n{site_url}/validate/delete/{token}\n',
            self.emali,
            [email],
            fail_silently=False,
        )

    def sign_up_email(self):
        send_mail(
            'Subject here',
            'Here is the message.',
            'tbaztw@gmail.com',
            ['tbaztw@gmail.com'],
            fail_silently=False,
        )