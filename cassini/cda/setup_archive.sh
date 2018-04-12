#!/bin/bash
set -e

if [ $# -lt 1 ] 
then
    echo "Usage: $(basename $0) directory-name"; 
    exit 1;
fi

VOLUME_ID=$1
ARCHIVE_DIR=/dsk1/www/html/archive/cocda/
ARCHIVE_FILE=${VOLUME_ID}.tar.gz 
SCRIPT_DIR=$(dirname $0)



#Unzip the archive file if it exists
if [ -a ${ARCHIVE_DIR}/${ARCHIVE_FILE} ] 
then
    echo "Extracting" $ARCHIVE_FILE
    pushd $ARCHIVE_DIR
    tar -xzf ${VOLUME_ID}.tar.gz
    chmod -R +r ${VOLUME_ID}
    popd
else
    echo "File not found:" ${ARCHIVE_DIR}/${ARCHIVE_FILE};
    exit 2;
fi

#If the file unzipped as expected, then generate the checksums and add the index.html files
if [ -d ${ARCHIVE_DIR}/${VOLUME_ID} ] 
then
    
    echo "Generating checksums"
    pushd ${ARCHIVE_DIR}
    md5deep -l -r ${VOLUME_ID} | sort -k2 > ${VOLUME_ID}_checksums.txt
    #use the following line instead if md5deep is not available:
    #find ${VOLUME_ID} -type f -exec md5sum '{}' \; | sort -k2 > ${VOLUME_ID}_checksums.txt

    popd
    
    echo "Copying index.html to data directories"
    find ${ARCHIVE_DIR}/${VOLUME_ID}/DATA -type d | grep "SIGNALS" | xargs -n1 cp ${SCRIPT_DIR}/index.html
else
    echo "Directory not found :" ${ARCHIVE_DIR}/${VOLUME_ID};
    exit 3;
fi

