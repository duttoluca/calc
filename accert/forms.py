from datetime import date

from django import forms


class AccertamentoForm(forms.Form):
    tassa = forms.FloatField(label='Tassa',
                             min_value=0.01)
    versato = forms.FloatField(label='Somma Importi Versati',
                               initial=0.0,
                               min_value=0.0)
    ugup = forms.DateField(label='UGUP (considerando proroghe pagamento)', input_formats=['%d/%m/%Y'])
    data_pagamento = forms.DateField(label='Data Pagamento',
                                     input_formats=['%d/%m/%Y'])
    data_calcolo = forms.DateField(label='Data Calcolo',
                                   input_formats=['%d/%m/%Y'],
                                   initial=date.today(),
                                   required=False)
    flag_sprint = forms.BooleanField(label='Emesso ante 06/07/2011 (verificare cartolina)',
                                     required=False)
