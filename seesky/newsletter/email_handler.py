from django.core.mail import send_mail
from seesky.settings import EMAIL_ADDRESS


class EmailHandler:
    """
    Class handles sending e-mails with the correct content.
    """
    def __init__(self):
        self.emali = EMAIL_ADDRESS

    def validation(self, email: str, token: str, name: str, site_url: str):
        """
        Method sends an email to the user with a confirmation link.
        :param email: user email
        :param token: unique token
        :param name: user name
        :param site_url: absolut webpage address
        :return: none
        """
        subject = 'Potwierdzenie emaila'
        message = f'Witaj {name}.\nZapisałeś się na newsletter, aby potwierdzić swój email kliknij w poniższy link\n"'\
            f'{site_url}/validate/{email}/{token}\n'\
            f'Jeśli to nie Ty zapisałeś się na newsletter, zignoruj ten email\n'\
            f'aby wypisać się z newslettera kliknij na poniższy link\n{site_url}/validate/delete/{token}\n'
        send_mail(subject, message, self.emali, [email], fail_silently=False)

    def newsletter_email(self, obj, sat, sunset, sunrise):
        """
        Method based on user data stored in the database, information about space objects and sunrise
        and sunset in the user's location send newsletter email.
        :param obj: object from db with information about user
        :param sat: list of dict witch information about objects in space
        :param sunset: sunset time
        :param sunrise: sunrise time
        :return: none
        """
        message = f'Witaj {obj.name}.\n' \
                  f'Informacje dla twojego miejsca:\n{obj.place}\n' \
                  f'Zachód słońca - {sunset}, Wschód słońca{sunrise}\n' \
                  f'Informacje o obiektach kosmicznych:\n'

        for poz in sat:
            message += f'Obiekt {poz.get("obj_short")} poruszający się w kierunku ' \
                f'{poz.get("obj_dir")} ({poz.get("obj_dir_angle")}°) z prędkością {poz.get("obj_speed")}km/min.' \
                f'\nNajbliżej Ciebie obiekt będzie ok {poz.get("obj_time")} (UTC) w kierunku ' \
                f'{poz.get("observation_dir")} ({poz.get("observation_dir_angle")}°) w odległości ' \
                f'{poz.get("obj_dist")}km.\n'
        subject = 'Newsletter SeeSky.pl.'
        send_mail(subject, message, self.emali, [obj.email], fail_silently=False)
