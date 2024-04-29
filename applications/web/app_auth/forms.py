from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Passwords do not match. Please enter the same password in both fields."),
        'required': _("This text is required."),
    }

    username = forms.CharField(
        help_text=_("(Required)"),
        label=False,
        max_length=12,
        error_messages={
            'required': _("* The username field is required!"),
        },
        widget = forms.TextInput(
            attrs={
                "autocomplete":"off",
                'placeholder':'Your username',
                'class': 'form-control',
            }
        )
    )

    password1 = forms.CharField(
        label=False,
        widget = forms.PasswordInput(
            attrs={
                'placeholder':'Password',
                'class': 'form-control',
            }
        ),
        help_text=_("(Required. At least 8 characters)"),
        error_messages={
            'required': _("* This field is required!"),
        },
    )

    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Confirm password',
                'class': 'form-control',
            }
        ),
        strip=False,
        help_text=_("(Required)"),
        error_messages={
            'required': _("* This field is required!"),
        },
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

##End_class


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', "autocomplete":"off"}
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', "autocomplete":"off"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        # Here you can perform additional validations on the backend if necessary
        return cleaned_data
    #end_def

## End_class