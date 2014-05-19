from django import forms
from django.utils.translation import ugettext as _

from account.models import EmailAddress

from kaleo.models import JoinInvitation


class InviteForm(forms.Form):
    email_address = forms.EmailField(label=_("Email"),)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(InviteForm, self).__init__(*args, **kwargs)

    def clean_email_address(self):
        email = self.cleaned_data["email_address"]
        if EmailAddress.objects.filter(email=email, verified=True).exists():
            raise forms.ValidationError(_("Email déjà en vigueur!"))
        elif JoinInvitation.objects.filter(from_user=self.user, signup_code__email=email).exists():
            raise forms.ValidationError(_("Vous avez déjà invité cet ami!"))
        return email
