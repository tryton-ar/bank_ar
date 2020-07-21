#!/usr/bin/env python
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import csv
import os
import sys

from argparse import ArgumentParser
from io import BytesIO, StringIO
from trytond.tools import file_open

try:
    from progressbar import ProgressBar, Bar, ETA, SimpleProgress
except ImportError:
    ProgressBar = None

try:
    from proteus import Model, config
except ImportError:
    prog = os.path.basename(sys.argv[0])
    sys.exit("proteus must be installed to use %s" % prog)


def fetch():
    sys.stderr.write('Fetching')
    with file_open('bank_ar/scripts/bank_ar.csv', mode='rb') as fp:
        data = fp.read()
    return data


def import_(data):
    Party = Model.get('party.party')
    Address = Model.get('party.address')
    Bank = Model.get('bank')
    Country = Model.get('country.country')
    Subdivision = Model.get('country.subdivision')
    print('Importing', file=sys.stderr)

    def get_country(code):
        country = countries.get(code)
        if not country:
            country, = Country.find([('code', '=', code)])
            countries[code] = country
        return country
    countries = {}

    def get_subdivision(country, code):
        code = '%s-%s' % (country, code)
        subdivision = subdivisions.get(code)
        if not subdivision:
            try:
                subdivision, = Subdivision.find([('code', '=', code)])
            except ValueError:
                return
            subdivisions[code] = subdivision
        return subdivision
    subdivisions = {}

    if ProgressBar:
        pbar = ProgressBar(
            widgets=[SimpleProgress(), Bar(), ETA()])
    else:
        pbar = iter
    f = StringIO(data.decode('utf-8'))
    records = []
    for row in pbar(list(csv.DictReader(
                    f, fieldnames=_fieldnames, delimiter=';'))):
        if row['country'] == 'country':
            continue
        country = get_country(row['country'])
        subdivision = get_subdivision(row['country'], row['subdivision'])
        zip = row['zip']
        bcra_code = row['bcra_code']
        print(bcra_code, file=sys.stderr)
        try:
            bank, = Bank.find([('bcra_code', '=', bcra_code)])
        except:
            party = Party(name=row['name'])
            party.vat_number = row['vat_number']
            party.iva_condition = 'responsable_inscripto'
            party.addresses.pop()
            party.addresses.append(Address(street=row['street'],
                    zip=row['zip'], city=row['city'], country=country,
                    subdivision=subdivision))
            party.save()
            record = Bank(bcra_code=row['bcra_code'], bic=row['bic'],
                          party=party)
            records.append(record)
    Bank.save(records)


_fieldnames = ['name', 'bic', 'bcra_code', 'vat_number', 'street',
    'zip', 'city', 'subdivision', 'country']


def main(database, config_file=None):
    config.set_trytond(database, config_file=config_file)
    do_import()


def do_import():
    data = fetch()
    import_(data)


def run():
    parser = ArgumentParser()
    parser.add_argument('-d', '--database', dest='database')
    parser.add_argument('-c', '--config', dest='config_file',
        help='the trytond config file')

    args = parser.parse_args()
    if not args.database:
        parser.error('Missing database')
    main(args.database, args.config_file)


if __name__ == '__main__':
    run()
