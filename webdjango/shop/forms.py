from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.core.validators import MinLengthValidator
from django.forms import ModelForm, Textarea
from markdownx.fields import MarkdownxFormField
from PIL import Image

# from bootstrap_datepicker_plus import DatePickerInput
from zxcvbn_password.fields import PasswordConfirmationField, PasswordField

from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": Textarea(attrs={"cols": 20, "rows": 5}),
        }
