#!/usr/bin/env python

import sys
import MySQLdb
import MySQLdb.cursors
import json
import os.path
import time

#print "arg number:", len(sys.argv)
#print "args:", str(sys.argv)
BOARD1_NAME = "flywatch_image1"
BOARD3_NAME = "flywatch_image3"
BOARD4_NAME = "flywatch_image4"

def selectArticles(db, boardName):
	cursor = db.cursor()
	cursor.execute('SELECT * FROM articles WHERE board = %s ORDER BY created_at DESC LIMIT 18',
					args = [boardName])
	return cursor.fetchall()

def extractBoardSpecifiedItems(jsonData, boardName):
	data = list()
	for d in jsonData:
		parameters = d["url"].split('?')[1].split('&')
		codeValue = ""
		for param in parameters:
			if param.startswith("code"):
				codeValue = param.split('=')[1]
				break

		if codeValue == boardName:
			data.append(d)

	return data

def sortByCreatedTime(list, reverse = True):
	return sorted(list, key = lambda k: k['createdAt'], reverse = reverse)

def insertArticle(connection, boardName, article):
	cursor = connection.cursor()
	print "Title of article to be inserted:", article['title']
	try:
		cursor.execute('SET NAMES utf8;')
		cursor.execute('INSERT INTO articles(board, title, content, url, created_at) \
						VALUES(%s, %s, %s, %s, %s);', 
						(boardName, article['title'].encode('utf-8'),
						article['content'].encode('utf-8'),
						article['url'], article['createdAt']))
		connection.commit()
		print "An article is inserted."
	except Exception, error:
		print Exception, error
		connection.rollback()

def insertLatestArticles(connection, dbData, boardName, jsonData):
	for article in jsonData:
		if len(dbData) == 0:
			insertArticle(connection, boardName, article)
		else:
			for row in dbData:
				if article['createdAt'].encode('utf-8') > row['created_at'] or \
					(article['createdAt'].encode('utf-8') == row['created_at'] and \
						article['title'].encode('utf-8') != row['title']):
					insertArticle(connection, boardName, article)
				else:
					break


if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
	print "Please check arguments. The argument should be a existing json file."
	sys.exit(1)

jsonFile = open(sys.argv[1], 'r')
jsonData = json.loads(jsonFile.read())
jsonFile.close()

board1_list = sortByCreatedTime(extractBoardSpecifiedItems(jsonData, BOARD1_NAME))
board3_list = sortByCreatedTime(extractBoardSpecifiedItems(jsonData, BOARD3_NAME))
board4_list = sortByCreatedTime(extractBoardSpecifiedItems(jsonData, BOARD4_NAME))

conn = MySQLdb.connect('mysql_host', 'id', 'pass', 'db', cursorclass = MySQLdb.cursors.DictCursor)
image1_data = selectArticles(conn, BOARD1_NAME)
image3_data = selectArticles(conn, BOARD3_NAME)
image4_data = selectArticles(conn, BOARD4_NAME)

insertLatestArticles(conn, image1_data, BOARD1_NAME, board1_list)
insertLatestArticles(conn, image3_data, BOARD3_NAME, board3_list)
insertLatestArticles(conn, image4_data, BOARD4_NAME, board4_list)
	
conn.close()