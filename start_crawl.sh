#!/bin/bash

NOW=`date '+%Y%m%d_%H%M'`
DATE=`date '+%Y%m%d'`
DIR="json/${DATE}"
JSON_FILE="flywatch_${NOW}.json"

if [ ! -d ${DIR} ]
then
	echo "${DIR} directory is not exists."
	mkdir -p ${DIR}
else
	echo "${DIR} directory is exists already."
fi

echo "Start crawling for flywatch."
scrapy crawl flywatch -o ${DIR}/${JSON_FILE}
echo "End crawling."

# write to db