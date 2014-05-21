from datetime import date

from django import forms


class AccertamentoForm(forms.Form):
    tassa = forms.FloatField(label='Tassa',
                             min_value=0.0)
    versato = forms.FloatField(label='Importo Versato',
                               initial=0.0,
                               min_value=0.0)
    ugup = forms.DateField(label='UGUP', input_formats=['%d/%m/%Y'])
    data_pagamento = forms.DateField(label='Data Pagamento',
                                     input_formats=['%d/%m/%Y'])
    data_calcolo = forms.DateField(label='Data Calcolo',
                                   input_formats=['%d/%m/%Y'],
                                   initial=date.today(),
                                   required=False)
    flag_sprint = forms.BooleanField(label='Accertamento emesso prima del 06/07/2011',
                                     required=False)


test_data = {'tassa': 100,
             'ugup': date(2007, 02, 02),
             'data_pagamento': date(2008, 02, 02),
             'flag_sprint': True}

test_data2 = {'tassa': 100,
             'ugup': date(2007, 02, 02),
             'data_pagamento': date(2008, 02, 02),
             'flag_sprint': False,
             'data_calcolo': date(2014, 05, 05),
             'versato': 99.99}
