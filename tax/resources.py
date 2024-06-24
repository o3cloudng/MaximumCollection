from import_export import resources
from tax.models import Permit


class BookResource(resources.ModelResource):

    class Meta:
        model = Permit
        fields = ('infra_type', 'amount', 'add_from', 'add_to', 'length', 'year_installed', 'upload_application_letter',
                  'upload_asBuilt_drawing', 'upload_payment_receipt')