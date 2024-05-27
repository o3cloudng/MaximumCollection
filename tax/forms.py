from django import forms
from tax.models import Permit, InfrastructureType
from django import forms


# class PermitForm(forms.ModelForm):
#     infra_type = forms.CharField(max_length=50, required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Infrastructure Type")
    
#     add_from = forms.CharField(max_length=50, required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Address from")
    
#     add_to = forms.CharField(max_length=50, required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Address to")
    
#     length = forms.CharField(max_length=50, required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Length")
    
#     year_installed = forms.CharField(max_length=50, required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Year of installation")
    
#     upload_application_letter = forms.FileField(required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Upload application letter")
    
#     upload_asbuilt_drawing = forms.FileField(required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Upload as-built drawing")
    
#     upload_payment_receipt = forms.FileField(required=True,
#         widget=forms.widgets.Input(attrs={
#                                          'class': "form-control form-select text-center",
#                                      }), label="Upload payment receipt")
#     class Meta:
#         model = Permit
#         fields = ['infra_type', 'add_from', 'add_to', 'length', 'year_installed', 'upload_application_letter',
#                   'upload_asbuilt_drawing', 'upload_payment_receipt']
    


class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        # fields = ['company', 'referenceid', 'infra_type', 'amount', 'add_from', 'add_to', 'length', 'year_installed', 'upload_application_letter',
        #           'upload_asBuilt_drawing', 'upload_payment_receipt']
        fields = ['infra_type', 'amount', 'add_from', 'add_to', 'length', 'year_installed', 'upload_application_letter',
                  'upload_asBuilt_drawing', 'upload_payment_receipt']

        widgets = {
            # 'company': forms.HiddenInput(attrs={'value' : '{{company}}'}),
            # 'referenceid': forms.HiddenInput(attrs={'value' : '{{referenceid}}'}),
            'infra_type': forms.Select(
                choices = InfrastructureType.objects.all(), 
                attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Infrastructure Type'
                }),
            'amount': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'required': False,
                'placeholder': 'Amount',
                'type': "number"
                }),
            'length': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 150px;',
                'placeholder': 'Length',
                'required': False,
                'type': "number"
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
                'required': False,
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