import glob
from argparse import ArgumentParser
from simfile import Simfile


def main(pack_path):
    packname = pack_path.split('/')[-1] if pack_path.split('/')[-1] else pack_path.split('/')[-2]
    simpaths = glob.iglob(f'{pack_path}/*/*.sm')
    sims = [Simfile(path) for path in simpaths]
    for sim in sims:
        # Song properties:
        # title [maintitle]
        # subtitle
        # artist
        # displaybpm [bpm]
        for chart in sim.charts:
            pass


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('pack_path', type=str)

    args = ap.parse_args()
    main(args.pack_path)

