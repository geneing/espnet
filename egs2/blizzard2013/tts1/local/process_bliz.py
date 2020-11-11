#!/usr/bin/env python3

import os
import argparse
import csv


def read_data( source_dir ):
    utt=[]
    str=[]
    fpath=[]
    with open(os.path.join(source_dir, 'all.txt'), 'r') as f:
        reader = csv.reader(f, delimiter='|')
        max_rows = 30000
        skipped = 0
        for row in reader:
            filepath = os.path.join(source_dir, row[1])
            if( len(row[2]) > 40 and os.path.getsize(filepath)>40000 ):
                utt.append(row[0])
                fpath.append(filepath)
                str.append(row[2])
                max_rows-=1
                if max_rows<=0:
                    break
            else:
                skipped += 1
    print("\n\nSkipped: %d\n\n"%skipped)
    return (utt,fpath,str)

def save_data(a, utt, fpath, str):
    with open(a.text, 'w') as f:
        for u, s in zip(utt, str):
            f.write('%s %s\n'%(u,s))

    with open(a.scp, 'w') as f:
        for u, fp in zip(utt, fpath):
            f.write('%s %s\n' % (u, fp))

    with open(a.spk2utt, 'w') as f:
        f.write("LJ ")
        for u in utt:
            f.write('%s '%(u))
        f.write("\n")

    with open(a.utt2spk, 'w') as f:
        for u in utt:
            f.write('%s LJ\n' % (u))


def main():
    print('Initializing Training Process..')

    parser = argparse.ArgumentParser()

    parser.add_argument('--scp', default="data/train/wav.scp")
    parser.add_argument('--utt2spk', default='data/train/utt2spk')
    parser.add_argument('--spk2utt', default='data/train/spk2utt')
    parser.add_argument('--text', default='data/train/text')
    parser.add_argument('--source-dir', default='/mnt/local/TrainingData/Blizzard2013_Aligned/')

    a = parser.parse_args()

    (utt, fpath, str) = read_data(a.source_dir)
    save_data(a, utt, fpath, str)

if __name__ == '__main__':
    main()