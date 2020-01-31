def parse_data(file='elem.txt'):
    """

    :param file:
    :return:
    """
    import json
    import re
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        # the data is malformatted with double quotes everywhere. Needs serios parsing.
        # remove starting and trailing {, }
        text = text[1:-1]
        # the first 2 elements are `result` and `lang`. The 3rd element is `rows`, a list of interesting data
        text = text.split(',', 2)
        data = dict()
        for elem in text:  # should have 3 elements in text
            tmp = elem.replace("\"", "").split(':', 1)
            data[tmp[0]] = tmp[1]
        # now the difficult bit - parse the `data["rows"]`.
        # it is a list of dictionaries, usually well-formatted except with some double-quotes in fields, but no quote around keys and data
        # strategy is based on the fact that the keys in all dicts are identical and in same order:
        # criusr, fax, name, officehour, code, tel, agreementpharmacy, vieworder, chgdate, maskstock,
        # address_p, name_p, nightpharmacy, address, void, viewstat, cridate, id, chgusr
        tb = data['rows']
        # remove heading and trailing square bracket
        tb = tb.lstrip('[').rstrip(']')

        pattern = '\{criusr:(.*?),fax:(.*?),name:(.*?),officehour:(.*?),code:(.*?),tel:(.*?),officehour_p:(.*?),agreementpharmacy:(.*?),vieworder:(.*?),chgdate:(.*?),maskstock:(.*?),address_p:(.*?),name_p:(.*?),nightpharmacy:(.*?),address:(.*?),void:(.*?),viewstat:(.*?),cridate:(.*?),id:(.*?),chgusr:(.*?)}'
        print(tb)

parse_data()
