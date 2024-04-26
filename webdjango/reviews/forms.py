from django.forms import ModelForm, Textarea
from reviews.models import Review
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['user_name','rating','comment']
        widgets = {
            'comment':Textarea(attrs={'cols':40,'rows':15}),
        }




        
"""

sdfuygdfrom django.forms import ModelForm, Textarea
from reviews.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 60, 'rows': 20}),  # Tăng kích thước của ô nhập liệu
        }

    def clean_rating(self):
        # Kiểm tra xem rating có nằm trong phạm vi từ 1 đến 5 không
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating




"""