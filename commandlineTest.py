import argparse,sys

parser = argparse.ArgumentParser(
    description='sum the integers at the command line')
parser.add_argument(
    'integers', metavar='int', nargs='+', type=int,
    help='an integer to be summed')
parser.add_argument(
    '--log', default=sys.stdout, type=argparse.FileType('w'),
    help='the file where the sum should be written')
parser.add_argument('--n' ,type=str)
parser.add_argument('--name' ,type=str,default='nameDefault')


args = parser.parse_args()
print('begin:')
print(args.integers ,args.n ,args.name)

# args.log.write('%s' % sum(args.integers))
# args.log.close()

