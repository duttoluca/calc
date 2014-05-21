from datetime import date
from math import trunc

from dateutil.relativedelta import relativedelta

from django.shortcuts import render, render_to_response

from forms import AccertamentoForm
from django.core.urlresolvers import reverse
# 
# #sanzioni
# if flag_sprint:
#     if DAYS <= 14:
#         SANZIONE_CALC = round(((float(TAX) - float(TAX_VERSATA)) / 100) * (DAYS * 2), 2)
#     else:
#         SANZIONE_CALC = round(((float(TAX) - float(TAX_VERSATA)) / 100) * 30.0, 2)
# else:
#     SANZIONE_CALC = round(((float(TAX) - float(TAX_VERSATA)) / 100) * 30.0, 2)
# #interessi
# if TIPO_ACCERT == 1:
#     INTERESSE_CALC = round(((float(TAX) - float(TAX_VERSATA)) / 100) * 1.375 * trunc((YEARS * 12 + MONTHS) / 6), 2)
# elif TIPO_ACCERT == 2:
#     INTERESSE_CALC = round((float(TAX) / 100) * 1.375 * trunc((YEARS * 12 + MONTHS)/6), 2)
# elif TIPO_ACCERT == 3:
#     INTERESSE_CALC = round(((float(TAX) - float(TAX_VERSATA)) / 100) * 1.375 * trunc((YEARS_A * 12 + MONTHS_A) / 6), 2)
# elif TIPO_ACCERT == 4:
#     int_a = round(((float(TAX) - float(TAX_VERSATA)) / 100) * 1.375 * trunc((YEARS_A * 12 + MONTHS_A) / 6), 2)
#     int_b = round((float(TAX) / 100) * 1.375 * trunc((YEARS * 12 + MONTHS) / 6), 2)
#     INTERESSE_CALC = int_a + int_b
# else:
#     print "boh"


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
            data = {}
            t, i, s = tassa - versato, 0, 0
            # calcolo interessi
            tipo = -1
            if versato == 0 and data_pagamento > ugup:
                i = round((t / 100) * 1.375 * trunc((anni_pagamento * 12 + mesi_pagamento) / 6), 2)
                tipo = 1
            elif tassa == versato and data_pagamento > ugup:
                i = round((tassa / 100) * 1.375 * trunc((anni_pagamento * 12 + mesi_pagamento) / 6), 2)
                tipo = 2
            elif tassa > versato and data_pagamento <= ugup:
                i = round((t / 100) * 1.375 * trunc((anni_calcolo * 12 + mesi_calcolo) / 6), 2)
                tipo = 3
            elif tassa > versato and data_pagamento > ugup and data_calcolo is not None:
                i = round(((t / 100) * 1.375 * trunc((anni_calcolo * 12 + mesi_calcolo) / 6)) + ((tassa / 100) * 1.375 * trunc((anni_pagamento * 12 + mesi_pagamento) / 6)), 2)
                tipo =  4
            else:
                #errore nella casistica, gestire
                return render(request, 'calcola.html', {'form': form, 'error': True})
            # calcolo sanzioni
            if flag_sprint and giorni_pagamento <= 14:
                if tipo != 3:
                    s = round((tassa / 100) * (giorni_pagamento * 2), 2)
                else:
                    s = round((t / 100) * (giorni_pagamento * 2), 2)
            else:
                if tipo != 3:
                    s = round((tassa / 100) * 30, 2)
                else:
                    s = round((t / 100) * 30, 2)

            data['tassa'] = t
            data['interesse'] = i
            data['sanzione'] = s
            data['totale'] = t + i + s
            return render(request, 'calcola.html', {'form': AccertamentoForm(), 'data': data})
    else:
        form = AccertamentoForm()

    return render(request, 'calcola.html', {'form': form, })
