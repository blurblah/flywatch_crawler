#!/bin/bash

NOW=`date '+%Y%m%d_%H%M'`
DATE=`date '+%Y%m%d'`
PWD="$(dirname ${BASH_SOURCE[0]})"
DIR="${PWD}/json/${DATE}"
LOG_DIR="${PWD}/logs"
JSON_FILE="flywatch_${NOW}.json"

if [ ! -d ${DIR} ]
then
	echo "${DIR} directory is not exists."
	mkdir -p ${DIR}
else
	echo "${DIR} directory is exists already."
fi

echo "#### Start crawling for flywatch ####"
scrapy crawl flywatch -o ${DIR}/${JSON_FILE}
CODE=$?
if [ ${CODE} -ne 0 ]
then
	exit ${CODE}
fi
echo "#### End crawling ####"

# write to db
echo "#### Start DB update... ####"
python json_uploader.py ${DIR}/${JSON_FILE}
echo "#### End of update ####"