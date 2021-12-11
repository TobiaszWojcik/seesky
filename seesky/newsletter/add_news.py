import re
from .models import Newsletter
from django.db.utils import IntegrityError
from .email_handler import EmailHandler

class ValidEmail:

    @staticmethod
    def confirm (email, token):
        obj = Newsletter.objects.filter(token=token)
        if obj:
            if email == "delete":
                email = obj[0].email
                obj.delete()
                return f"Email {email} został usunięty z newslettera"
            elif obj[0].email == email:
                if obj[0].valid:
                    return "Ten email został już potwierdzony"
                else:
                    obj.update(valid=True)
                    return f'Gratuluję, email {email} został potwierdzony!'

        return "Nieprawidłowe dane!"


class NewsletterSave:
    def __init__(self, post_dict):
        self.error = None
        self.name = post_dict.get('name')
        self.email = post_dict.get('email')
        self.place = post_dict.get('place_name')
        self.lat = post_dict.get('lat')
        self.lon = post_dict.get('lon')
        self.token = post_dict.get('csrfmiddlewaretoken')
        self.time = post_dict.get('time')

    def __savedb(self):
        db = Newsletter(
            name=self.name,
            place=self.place,
            lat=self.lat,
            lon=self.lon,
            email=self.email,
            token=self.token,
            email_time=self.time
        )
        db.save()

    def check(self, site):
        if not re.match(r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", self.email):
            self.error = "Podałeś niepoprawny email"
            return False
        if not re.match(r"([a-zA-Z0-9_\-\. ])", self.name):
            self.error = "W nazwie są niedozwolone znaki"
            return False
        try:
            email = EmailHandler()
            email.validation(self.email, self.token, self.name, site)
            self.__savedb()
            return True

        except IntegrityError:
            self.error = "Podany email jest już w bazie, aby dodać ten email usuń go wcześniej z newslettera"
            return False

