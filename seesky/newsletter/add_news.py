import re
from .models import Newsletter
from django.db.utils import IntegrityError
from .email_handler import EmailHandler


class ValidEmail:
    """
    The class checks the information in the link and approve the user or delete the user.
    """

    @staticmethod
    def confirm (email: str, token: str):
        """
        Handles the link and on its basis it validates the data and performs the called action.
        :param email: string, adress email or "delete" fraze for delete user action
        :param token: string, unique token fraze
        :return: string, result of the action taken
        """
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
    """
    Class NewsletterSave Handles subscription to the newsletter.
    """
    def __init__(self, post_dict):
        """
        Method intercepts the data needed for the correct handling of the newsletter.
        :param post_dict:
        dictionary with:'name', 'email', 'place_name', 'lat', 'lon', 'csrfmiddlewaretoken', 'time' keys
        """
        self.error = None
        self.name = post_dict.get('name')
        self.email = post_dict.get('email')
        self.place = post_dict.get('place_name')
        self.lat = post_dict.get('lat')
        self.lon = post_dict.get('lon')
        self.token = post_dict.get('csrfmiddlewaretoken')
        self.time = post_dict.get('time')

    def __savedb(self):
        """
        Method save information to db
        """
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
        """
        Method checks the correctness of the provided data and whether the given e-mail already exists in the database.
        Creates error information of the form self.error.
        :param site: absolut webpage adress
        :return: boolean 'True' if the data are correct else 'False'
        """
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

