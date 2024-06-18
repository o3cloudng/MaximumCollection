from django import forms
from tax.models import Permit, InfrastructureType, Waver
from django import forms


class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = ['infra_type', 'amount', 'add_from', 'add_to', 'length', 'year_installed', 'upload_application_letter',
                  'upload_asBuilt_drawing', 'upload_payment_receipt']

        widgets = {
            'infra_type': forms.Select(
                choices = InfrastructureType.objects.all(), 
                attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': True,
                'placeholder': 'Infrastructure Type'
                }),
            'amount': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Amount',
                'value': 0,
                'type': "text"
                }),
            'length': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'placeholder': 'Length',
                'required': False,
                'type': "text"
                }),
            'add_from': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Address from'
                }),
            'add_to': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Address to'
                }),
            'year_installed': forms.DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': True,
                'placeholder': 'Year of installation',
                'type':"Date"
                }),
            'upload_application_letter': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 50px;',
                'required': False,
                'placeholder': 'Upload application letter'
                }),
            'upload_asBuilt_drawing': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Upload as-built drawing'
                }),
            'upload_payment_receipt': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Upload payment receipt'
                }),
        }

    def __init__(self, *args, **kwargs):
        #  question_id = kwargs.pop('question_id')
         super().__init__(*args, **kwargs)
         self.fields['infra_type'] = forms.ModelChoiceField(
             queryset=InfrastructureType.objects.all(),
             widget=forms.Select(attrs={'class': 'form-control select2', 'placeholder':'Infrastructure'})
         )

class PermitEditForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = ['infra_type', 'referenceid', 'amount', 'add_from', 'add_to', 'length', 'year_installed', 'upload_application_letter',
                  'upload_asBuilt_drawing', 'upload_payment_receipt', 'is_disputed', 'is_revised', 'is_paid']

        widgets = {
            'infra_type': forms.Select(
                choices = InfrastructureType.objects.all(), 
                attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': True,
                'placeholder': 'Infrastructure Type'
                }),
            'amount': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Amount',
                'type': "text"
                }),
            'referenceid': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': True,
                'placeholder': 'Amount',
                'type': "hidden"
                }),
            'length': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'placeholder': 'Length',
                'required': False,
                'type': "text"
                }),
            'add_from': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Address from'
                }),
            'add_to': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Address to'
                }),
            'year_installed': forms.DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': True,
                'placeholder': 'Year of installation',
                'type':"Date"
                }),
            'upload_application_letter': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Upload application letter'
                }),
            'upload_asBuilt_drawing': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Upload as-built drawing'
                }),
            'upload_payment_receipt': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Upload payment receipt'
                }),
        }

    def __init__(self, *args, **kwargs):
        #  question_id = kwargs.pop('question_id')
         super().__init__(*args, **kwargs)
         self.fields['infra_type'] = forms.ModelChoiceField(
             queryset=InfrastructureType.objects.all(),
             widget=forms.Select(attrs={'class': 'form-control select2', 'placeholder':'Infrastructure'})
         )


class WaverForm(forms.ModelForm):
    class Meta:
        model = Waver
        fields = ['referenceid', 'wave_amount', 'receipt']

        widgets = {
            'referenceid': forms.TextInput(
                attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'required': False,
                'type': 'hidden'
                }),
            'wave_amount': forms.TextInput(
                attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'required': True,
                'placeholder': 'Amount paid'
                }),
            'receipt': forms.FileInput(
                attrs={
                'class': "form-control",
                'style': 'max-width: 100%;',
                'required': True,
                'placeholder': 'Upload receipt'
                })
        }