from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from django.contrib.admin import widgets

from myFinance.models import Tag, Transaction, Plan


class TransactionForm(forms.Form):
    name = forms.CharField(required=True)
    value = forms.CharField(required=True)
    date = forms.DateField(required=True, widget=widgets.AdminDateWidget)
    tag = forms.ChoiceField(required=True, choices=[('', '------')])

    class Meta:
        model = Transaction
        fields = ('name', 'date', 'tag', 'value')

    def __init__(self, user, *args, **kwargs):
        # using kwargs
        super(TransactionForm, self).__init__(*args, **kwargs)
        # user = kwargs.pop('user', None)
        self.fields['tag'].choices = self.fields['tag'].choices + [(tag.name, tag.name) for tag in
                                                                   Tag.objects.filter(user=user)]


class IsBankStatements(forms.Form):
    is_bank_statement = forms.BooleanField()


class TransactionModelForm(BSModalForm):
    date = forms.ChoiceField(choices=zip(range(1, 30), range(1, 30)))

    class Meta:
        fields = ['date', ]


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ('tag', 'value',)

# class NewTransactionFormset(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(NewTransactionFormset, self).__init__(*args, **kwargs)
#
#     def _construct_forms(self):
#         self.forms = []
#         for i in range(self.total_form_count()):
#             self.forms.append(self._construct_form(i, user=self.user))
