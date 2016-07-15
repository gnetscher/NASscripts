# copy files from the previous day to videoArchive without overwriting
find '/volume1/video/' -mindepth 1 -type f -mtime -1 -exec cp -n '{}' '/volume1/videoArchive/' \;

# remove files older than 3 days 
find '/volume1/video/' -mindepth 1 -mtime +3 -exec rm -f '{}' \;
