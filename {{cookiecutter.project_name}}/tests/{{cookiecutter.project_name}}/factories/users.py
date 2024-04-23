from factorio.factories import Factory
from factorio.fields import FactoryField, Field

from {{cookiecutter.project_name}}.users.models import SignupToken, User


class UserFactory(Factory):
    class Meta:
        model = User

    class Fields:
        email = Field("email")


class SignupTokenFactory(Factory):
    class Meta:
        model = SignupToken

    class Fields:
        user = FactoryField(UserFactory)
