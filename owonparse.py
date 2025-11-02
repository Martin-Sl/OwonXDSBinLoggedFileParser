import argparse
from owon_bin_parser_hexview import parse

parser = argparse.ArgumentParser(description="OWON .bin quick parser")
parser.add_argument('file', help='OWON .bin file to parse')
parser.add_argument('--parseAll', help='parse all files in current directory', action='store_true')
parser.add_argument('--plot', action='store_true', help='do not plot')
parser.add_argument('--dump-header', action='store_true', help='print header fields')
args = parser.parse_args()

if args.parseAll:
    import glob
    bin_files = glob.glob("*.bin")
    for bf in bin_files:
        print(f"\n\nProcessing file: {bf}")
        parse(bf, plot=args.plot, dump_header=args.dump_header)
else:
    parse(args.file, plot=args.plot, dump_header=args.dump_header)