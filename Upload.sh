# mv high res video older than 2 days to archive
find '/volume1/highResVideo/' -type d -mtime +2 -exec mv '{}' '/volume1/videoArchive/' \;

# delete low res video older than 3 days from public and private folder
find '/volume1/video/' -type d -mtime +3 -exec rm -rf '{}' \;
find '/volume1/privateVideo/' -type d -mtime +3 -exec rm -rf '{}' \;

# push low res video from public and private folder to server
rsync -auP /volume1/video/ nestsense@nestsense.banatao.berkeley.edu:~/data/George/PilotSystemTest/
rsync -auP /volume1/privateVideo/ nestsense@nestsense.banatao.berkeley.edu:~/data/George/PilotSystemTest/
