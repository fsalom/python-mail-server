from django.contrib.auth.models import UserManager as DjangoUserManager

class UserManager(DjangoUserManager):
    def create(self, email, password, first_name='', **kwargs):
        BaseUserDBO = self.model
        new_user = BaseUserDBO(first_name=first_name, email=email, **kwargs)

        new_user.username = new_user.email
        new_user.set_password(password)

        new_user.save()
        return new_user
