#!/usr/bin/env python3

import save_manager
from argparse import ArgumentParser
from settings import CURRENCY_LIST


if __name__ == "__main__":
    # parse arguments
    parser = ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, required=True, help="The save file you want to work with")
    parser.add_argument("-o", "--out-file", type=str, default='account_modified.dat', help="The save file you want to output to")
    modifications_subparser = parser.add_subparsers(title='Modifications')
    currency_parser = modifications_subparser.add_parser(name='currency', help="Command to modify currency amounts.")
    arg_currencies = {}
    for id, currency in CURRENCY_LIST.items():
        curr_currency = currency.lower().replace(' ', '-')
        currency_parser.add_argument('--{0}'.format(curr_currency), type=int,
                                     help="Set amount of {0} to the specified amount".format(curr_currency))
    args = parser.parse_args()

    # instance account object
    account = save_manager.SaveData(args.in_file, args.out_file)
    # modify save file here
    account_currencies = account.currency_names
    for id, currency in CURRENCY_LIST.items():
        amount = None
        curr_currency = currency.lower().replace(' ', '-')
        try:
            amount = getattr(args, curr_currency)
        except AttributeError:
            pass
        if amount:
            account.set_currency(id, amount)


    # This should be the only write we do, a final commit_all_changes().
    account.commit_all_changes()
