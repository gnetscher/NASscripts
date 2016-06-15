import glob
import re
import argparse
import os
import pdb

def data_dir_2_file_paths(rootDir):
    extns = ['avi']
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for name in dirnames:
            head = str(dirpath) + '/' + str(name)
            for extn in extns:
                path = os.path.join(head, '*.' + extn)
                for fname in glob.iglob(path):
                    yield fname
        else:
            head = str(dirpath)
            for extn in extns:
                path = os.path.join(head, '*.' + extn)
                for fname in glob.iglob(path):
                    yield fname

if __name__ == '__main__':
    # define input args
    parser = argparse.ArgumentParser(
        description='Script to compress videos and add to either public or private folder',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--privateRooms', default=[], nargs='*', type=str,
                        help='1 or more private rooms each separated by a space')
    parser.add_argument('--privateDir', default='/volume1/privateVideo/', type=str,
                        help='The directory where the private room video should be stored')
    parser.add_argument('--inputDir', default='/volume1/highResVideo/', type=str,
                        help='The directory where high res videos are located')
    parser.add_argument('--publicDir', default='/volume1/video/', type=str,
                        help='The directory where the public room video should be stored')
    args = parser.parse_args() 
    
    inDir    = args.inputDir 
    pubDir   = args.publicDir
    priDir   = args.privateDir
    priRooms = args.privateRooms

    pgen = data_dir_2_file_paths(inDir)
    for p in pgen:
        # retrieve information about where to put compressed 
        basePath = re.sub(inDir, '', p)
        room = basePath.split('/')[0]
        fileName, fileExt = basePath.split('.')
        basePath = fileName + '.mp4'
        if room in priRooms:
            op = os.path.join(priDir, basePath)
        else:
            op = os.path.join(pubDir, basePath)
        if os.path.exists(op):
            continue
        outDir = os.path.dirname(op)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        print '~~~~~ Compressing {0} ~~~~~'.format(p)
        compressCmd = 'ffmpeg -i {0} -vcodec mpeg4 {1};'.format(p, op) 
        os.system(compressCmd)

