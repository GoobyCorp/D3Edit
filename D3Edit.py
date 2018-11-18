#!/usr/bin/env python3

import gui
import save_manager
import sys
from argparse import ArgumentParser
from settings import currency_list


if __name__ == "__main__":
    # parse arguments
    parser = ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, required=False, help="The save file you want to work with")
    parser.add_argument("-o", "--out-file", type=str, default='account_modified.dat',
                        help="The save file you want to output to")
    parser.add_argument("-g", "--gui", default=False, action='store_true', help="Launch GUI instead of CLI")
    mod_group = parser.add_argument_group("modifications")
    mod_group.add_argument('--all-currencies', type=int,
                           help="Set all currencies to this amount (overrides other changes)")
    # modifications_subparser = parser.add_subparsers(title='Modifications')
    # currency_parser = modifications_subparser.add_parser(name='currency', help="Command to modify currency amounts.")
    for id, currency in currency_list.items():
        curr_currency = currency.lower().replace(' ', '-')
        mod_group.add_argument('--{0}'.format(curr_currency), type=int,
                               help="Set amount of {0} to the specified amount".format(curr_currency))
        #    currency_parser.add_argument('--{0}'.format(curr_currency), type=int,
    args = parser.parse_args()

    # TESTING GUI
    if args.gui:
        gui.start()
        sys.exit(0)
    else:
        assert args.in_file, "Must specify a file when running in CLI mode."
    # instance account object
    account = save_manager.SaveData(args.in_file, args.out_file)
    # modify save file here
    if args.all_currencies:
        for id in currency_list.keys():
            account.set_currency(id, args.all_currencies)
    else:
        for id, currency in currency_list.items():
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
