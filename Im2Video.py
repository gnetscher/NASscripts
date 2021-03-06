import glob
import re
import argparse
import os
import pdb
from time import strftime, localtime

if __name__ == '__main__':
    # define input args
    parser = argparse.ArgumentParser(
        description='Script to create videos from images and add' 
                    'to either public or private folder',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--privateRooms', default=[], nargs='*', type=str,
                        help='1 or more private rooms each separated by a space')
    parser.add_argument('--privateDir', default='/volume1/privateVideo', type=str,
                        help='The directory where the private room video should be stored')
    parser.add_argument('--inputDir', default='/volume1/highResImages', type=str,
                        help='The directory where high res videos are located')
    parser.add_argument('--publicDir', default='/volume1/video', type=str,
                        help='The directory where the public room video should be stored')
    parser.add_argument('--tmpDir', default='/volume1/tmp', type=str,
                        help='The directory where the tmp images should be stored')
    args = parser.parse_args() 
    
    inDir    = args.inputDir 
    pubDir   = args.publicDir
    priDir   = args.privateDir
    priRooms = args.privateRooms
    tmpDir   = args.tmpDir
    imArDir  = '/volume1/highResImageArchive'

    cTime    = localtime()
    timePath = strftime("%Y%m%d/%H00", cTime)
    pHour    = int(timePath.split('/')[-1]) - 100
    pTimePath= timePath.split('/')[0] + '/' + str(pHour)
    
    # find latest images - not using os.walk to avoid walking all time directories
    for room in os.listdir(inDir):
        for cam in os.listdir(inDir + '/' + room):
            for i, tp in enumerate([timePath, pTimePath]): 
                # determine input path
                subPath = room + '/' + cam + '/' + tp
                inPath = inDir + '/' + subPath 
                if not os.path.exists(inPath):
    	            continue
                print '##### From {0} #####'.format(inPath)
                
                # move chunk for processing to tmp folder
                tmpPath = tmpDir + '/' + room + '/' + cam
                if not os.path.exists(tmpPath):
    	            os.system('mkdir -p {0}'.format(tmpPath))
                else:
                    os.system('rm -f ' + tmpPath + '/*')
                if glob.glob(inPath + '/*.jpg'): 
                    os.system('mv ' + inPath + '/*.jpg ' + tmpPath)
                else:
                    continue
     
                # perform video encoding
                tPathRegex = tmpPath + '/' + '*.jpg'
                pathRegex = '\"' + tPathRegex + '\"'
                imArPath = imArDir + '/' + subPath 
                if not os.path.exists(imArPath):
                    os.system('mkdir -p {0}'.format(imArPath))
                os.system('cp ' + tPathRegex + ' ' + imArPath) 
                videoFileName = room + '_' + cam + '_' + strftime("%Y%m%d_%H%M00", cTime) + '_' + str(i) + '.mkv'
                newVideoPath = tmpPath + '/' + videoFileName
                print '~~~~~~ Creating {0} ~~~~~~'.format(newVideoPath)
                imVidCmd = 'ffmpeg -y -hide_banner -loglevel warning -framerate 5 -pattern_type glob -i ' + pathRegex + ' -c:v mjpeg ' + newVideoPath
                os.system(imVidCmd)
     
                # prepare output path
    	        if room in priRooms:
    	            outPath = priDir + '/' + subPath
    	        else:
    	            outPath = pubDir + '/' + subPath 
    	        if not os.path.exists(outPath):
    	            os.system('mkdir -p {0}'.format(outPath))
                outVideoPath = outPath + '/' + videoFileName 
                oldVideoPath = glob.glob(outPath + '/*.mkv')
                if not oldVideoPath:
                    # no previous file - simply move new file
                    os.system('mv {0} {1}'.format(newVideoPath, outVideoPath))
                else:
                    # append to previous video from the hour
                    oldVideoPath = oldVideoPath[0]
                    concatFile = tmpPath + '/concatList.txt'
                    with open(concatFile, 'w') as f:
                        f.write('file \'{0}\'\nfile \'{1}\''.format(os.path.abspath(oldVideoPath), os.path.abspath(newVideoPath)))
                    concatCmd = "ffmpeg -y -hide_banner -loglevel warning -f concat -i {0} -c copy {1}".format(concatFile, outVideoPath)
                    os.system(concatCmd)
                    os.system('rm {0}'.format(oldVideoPath))
