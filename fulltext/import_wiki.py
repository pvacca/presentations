#!/usr/bin/python

import sys

if len(sys.argv) == 1:
    raise Exception('Let me know what to import, boss.')

infile = sys.argv[1]

import xml.etree.ElementTree as ET
import psycopg2

host="localhost"
port=5432
db="wiki"

con = psycopg2.connect("host='%s' port='%i' dbname='%s'" % (host, port, db))
t = ET.parse(infile)
root = t.getroot()
for e in root.iter('{http://www.mediawiki.org/xml/export-0.10/}page'):
    title = e.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
    id = e.find('{http://www.mediawiki.org/xml/export-0.10/}id').text
    content = e.find('{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text'
        ).text
    cur = con.cursor()
    try:
        data = (title, id, content)
        cur.execute("INSERT INTO pages VALUES(%s, %s, %s)", data)
    finally:
        con.commit()

con.close()
del con
del root
