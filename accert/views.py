from math import trunc

from dateutil.relativedelta import relativedelta

from django.shortcuts import render

from forms import AccertamentoForm


def calcolaAccert(request):
    template = 'calcola.html'
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
            t, i, s = tassa - versato, 0, 0
            # calcolo interessi
            if not versato and data_pagamento > ugup:
                i = round((t / 100) * 1.375 * trunc((anni_pagamento * 12 + mesi_pagamento) / 6), 2)
                tipo = 1
            elif tassa and tassa == versato and data_pagamento > ugup:
                i = round((tassa / 100) * 1.375 * trunc((anni_pagamento * 12 + mesi_pagamento) / 6), 2)
                tipo = 2
            elif tassa > versato and versato and data_pagamento <= ugup:
                i = round((t / 100) * 1.375 * trunc((anni_calcolo * 12 + mesi_calcolo) / 6), 2)
                tipo = 3
            elif tassa > versato and versato and data_pagamento > ugup and data_calcolo is not None:
                i = round(((t / 100) * 1.375 * trunc((anni_calcolo * 12 + mesi_calcolo) / 6)) + ((versato / 100) * 1.375 * trunc((anni_pagamento * 12 + mesi_pagamento) / 6)), 2)
                tipo = 4
            else:
                #errore nella casistica, gestire
                return render(request, template, {'form': form, 'error': True})
            # calcolo sanzioni
            if not flag_sprint and giorni_pagamento <= 14:
                if tipo != 3:
                    s = round((tassa / 100) * (giorni_pagamento * 2), 2)
                else:
                    s = round((t / 100) * (giorni_pagamento * 2), 2)
            else:
                if tipo != 3:
                    s = round((tassa / 100) * 30, 2)
                else:
                    s = round((t / 100) * 30, 2)
            # dizionario di ritorno
            data = {'tassa': t,
                    'interesse': i,
                    'sanzione': s,
                    'totale': t + i + s}
            return render(request, template, {'form': AccertamentoForm(), 'data': data})
    else:
        form = AccertamentoForm()

    return render(request, template, {'form': form})
