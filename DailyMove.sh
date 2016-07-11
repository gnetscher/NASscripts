# move files older than 3 days to the videoArchive for uploading
find '/nas_share/video/' -mindepth 1 -type f -mtime +3 -exec mv -f '{}' '/nas_share/videoArchive/' \;
