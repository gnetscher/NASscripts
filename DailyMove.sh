# copy files from the previous day to videoArchive
find '/nas_share/video/' -mindepth 1 -type f -mtime -1 -exec cp '{}' '/nas_share/videoArchive/' \;

# remove files older than 3 days 
find '/nas_share/video/' -mindepth 1 -mtime +3 -exec rm -f '{}' \;
