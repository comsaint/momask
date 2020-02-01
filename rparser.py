from settings import CUR_TIMESTAMP, DATA_FOLDER
import pandas as pd
import re


def parse_data(file):
    """
    Parse to Pandas DataFrame
    :param file:
    :return:
    """
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

        pattern = '\{criusr:(?P<criusr>.*?),fax:(?P<fax>.*?),name:(?P<name>.*?),officehour:(?P<officehour>.*?),code:(?P<code>.*?),tel:(?P<tel>.*?),officehour_p:(?P<officehour_p>.*?),agreementpharmacy:(?P<agreementpharmacy>.*?),vieworder:(?P<vieworder>.*?),chgdate:(?P<chgdate>.*?),maskstock:(?P<maskstock>.*?),address_p:(?P<address_p>.*?),name_p:(?P<name_p>.*?),nightpharmacy:(?P<nightpharmacy>.*?),address:(?P<address>.*?),void:(?P<void>.*?),viewstat:(?P<viewstat>.*?),cridate:(?P<cridate>.*?),id:(?P<id>.*?),chgusr:(?P<chgusr>.*?)}'
        data = re.finditer(pattern=pattern, string=tb, flags=re.S)
        # convert to list of dicts
        ld = list()
        for shop in data:
            ld.append(shop.groupdict())
        # ... then to Pandas Dataframe
        df = pd.DataFrame(ld)
        # add a timestamp column
        df['parsed_timestamp'] = CUR_TIMESTAMP
        return df


def write_parsed_file(df, path):
    # parse to csv
    df.to_csv(path, encoding='utf-8', index=False)
    return 0


def run_parser(path_to_input):
    df = parse_data(path_to_input)
    p = DATA_FOLDER / 'parsed_{}.csv'.format(CUR_TIMESTAMP)
    write_parsed_file(df, path=p)
    return p
