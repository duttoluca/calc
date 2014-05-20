from datetime import date
from math import trunc

from dateutil.relativedelta import relativedelta

from django.shortcuts import render, render_to_response

from forms import AccertamentoForm
from django.core.urlresolvers import reverse


def calcola(request):
    if request.method == 'POST':
        form = AccertamentoForm(request.POST)
        if form.is_valid():
            tassa = form.cleaned_data['tassa']
            versato = form.cleaned_data['versato']
            ugup = form.cleaned_data['ugup']
            data_pagamento = form.cleaned_data['data_pagamento']
            data_calcolo = form.cleaned_data['data_calcolo']
            flag_sprint = form.cleaned_data['flag_sprint']
            #calcolo giorni/mesi/anni relativamente al pagamento
            giorni_pagamento = (data_pagamento - ugup).days
            rel_pag = relativedelta(data_pagamento, ugup)
            mesi_pagamento, anni_pagamento = rel_pag.months, rel_pag.years
            #calcolo mesi/anni relativamente al calcolo
            rel_calc = relativedelta(data_calcolo, ugup)
            mesi_calcolo, anni_calcolo = rel_calc.months, rel_calc.years
            # return dati_calcolati
            data = {'tassa': tassa-versato}
            return render(request, 'calcola.html', {'form': AccertamentoForm(), 'data': data})
    else:
        form = AccertamentoForm()

    return render(request, 'calcola.html', {'form': form, })
