#!/usr/bin/env python3

import platform
from os import getcwd
from argparse import ArgumentParser
from settings import currency_list


def main():
    import gui
    import save_manager
    # parse arguments
    parser = ArgumentParser(description="A script to encrypt/decrypt and modify Diablo III saves")
    parser.add_argument("-i", "--in-file", type=str, help="The save file you want to work with")
    parser.add_argument("-o", "--out-file", type=str, default='account_modified.dat',
                        help="The save file you want to output to")
    parser.add_argument("-c", "--cli", action='store_true', default=False, help="Run in CLI mode instead of GUI.")
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

    # Initialize GUI
    if not args.cli:
        instanced_gui = gui.D3Edit()
        instanced_gui.start()

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
    account.commit_account_changes()


if __name__ == "__main__":
    venv_platforms = ['Linux', 'Darwin']
    running_os = platform.system()
    # activate Linux/Darwin venvs:
    if any(p in running_os for p in venv_platforms):
        print("activated linux venv")
        activate_this_file = "{}/venv/bin/activate_this.py".format(getcwd())
        exec(open(activate_this_file).read(), dict(__file__=activate_this_file))
    elif running_os == 'Windows':
        print("Activating Windows venv")
        activate_this_file = "{}\\winvenv\\Scripts\\activate_this.py".format(getcwd())
        exec(open(activate_this_file).read(), dict(__file__=activate_this_file))
    main()
