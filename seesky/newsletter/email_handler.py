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

    def newsletter_email(self, obj, sat, sunset, sunrise):
        message = f'Witaj {obj.name}.\n' \
                  f'Informacje dla twojego miejsca:\n{obj.place}\n' \
                  f'Zachód słońca - {sunset}, Wschód słońca{sunrise}\n' \
                  f'Informacje o obiektach kosmicznych:\n' \
                  f'{obj.token}'

        for poz in sat:
            message += f'Obiekt {poz.get("obj_short")} poruszający się w kierunku ' \
                f'{poz.get("obj_dir")} ({poz.get("obj_dir_angle")}°) z prędkością {poz.get("obj_speed")}km/min.' \
                f'\nNajbliżej Ciebie obiekt będzie ok {poz.get("obj_time")} (UTC) w kierunku ' \
                f'{poz.get("observation_dir")} ({poz.get("observation_dir_angle")}°) w odległości ' \
                f'{poz.get("obj_dist")}km.\n'

        send_mail(
            'Newsletter SeeSky.pl.',
            message,
            self.emali,
            [obj.email],
            fail_silently=False,
        )
