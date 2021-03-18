from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Client


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class EditClientData(UserChangeForm):

    class Meta:
        model = Client
        fields = ("name", "surname", "cellphone_number", "city", "street", "house_number", "flat_number", "zip_code")
