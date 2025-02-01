# -*- coding: utf-8 -*-

# validatore di date


def data_valida(data):
    """
    controlla che la data sia corretta
    formati consentiti:
      dd/mm/aaaa
      ddmmaaaa
    """

    import datetime

    data = data.replace("/", "")

    if len(data) == 8:
        gg = data[0:2]
        mm = data[2:4]
        aaaa = data[4:8]
    else:
        return False, "data errata"

    # verifico correttezza di gg, mm, aaaa
    try:
        print(gg, mm, aaaa)
        data = datetime.date(int(aaaa), int(mm), int(gg))
    except ValueError as e:
        print(e)
        return False, "{0}".format(e)

    # data valida!
    return True, gg + "/" + mm + "/" + aaaa


# test
# ~ print( data_valida('11071975') )
# ~ print( data_valida('11/07/1975') )
# ~ print( data_valida('11/07/75') )
# ~ print( data_valida('nico') )
# ~ print( data_valida('12345678as') )
# ~ print( data_valida('32132000') )
