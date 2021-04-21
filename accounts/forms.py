from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import IntegerField, CharField, BooleanField, ChoiceField
from .models import CustomUser, choises


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username')

    user_type = ChoiceField(choices=choises)
    address = CharField(max_length=500)
    picture = CharField(max_length=500)
    accept_terms = BooleanField()

    def save(self, commit=True):
        user = super().save(commit)
        profile = CustomUser(user_type=self.cleaned_data.get('user_type'),
                             address=self.cleaned_data.get('address'),
                             picture=self.cleaned_data.get('picture'),
                             accept_terms=self.cleaned_data.get('accept_terms'), )
        if commit:
            profile.save()
        return user


class EditProfileForm(UserChangeForm):
    user_type = ChoiceField(choices=choises)
    address = CharField(max_length=500)
    picture = CharField(max_length=500)
    accept_terms = BooleanField()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username', 'password', 'user_type', 'address', 'picture',
                  'accept_terms', 'is_active', 'is_staff', 'is_superuser', 'last_login')
