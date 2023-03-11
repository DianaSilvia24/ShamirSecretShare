import argparse
from split import *
from recompose import *

if __name__=="__main__":

    parse=argparse.ArgumentParser()
    parse.add_argument("-split", nargs=2, required=False, type=list, help="Toggle to split a file in multiple parts")
    parse.add_argument("-recompose", action=argparse.BooleanOptionalAction, type=bool, help="Toggle to rejoin a set of files")
    parse.add_argument('file', nargs = "+", type=str, help="The files you want to process")

    args=parse.parse_args()

    if (args.split is None and args.recompose is None) or (args.split and args.recompose):
        print("Please specify exactly one action!")
        exit(1)

    if not args.split is None:
        args.split = [int("".join(i)) for i in args.split]
        n = max(args.split)
        m = min(args.split)

        if args.file is None:
            print("Please specify the file you want to split!")
            exit(1)

        if len(args.file) != 1:
            print("Specify exactly one file to split!")
            exit(1)

        print("Acuma fac split la", args.file[0], "cu n =", n, "si m =", m)
        split_file(args.file[0], n, m)


    if not args.recompose is None:
        if len(args.file) < 2:
            print("Please specify at least two splits!")
            exit(1)

        recover_file(args.file)
