from django import forms
from accountbook.models import Account, Category


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['category', 'contents', 'date', 'amount']

        category = forms.ChoiceField(label='category')

        contents = forms.CharField(label='contents')

        date = forms.CharField(label='date')

        amount = forms.IntegerField(label='amount')


class CategoryRegisterer(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'flag']

        #category_id = forms.IntegerField(label='category_id')

        category = forms.CharField(label='category')

        flag = forms.CharField(label='flag')
