from __future__ import print_function
import psycopg2

file = 'Top 10 streets by state (2015).txt'
i = 0

host="localhost"
port=5432
db="x"

con = psycopg2.connect("host='%s' port='%i' dbname='%s'" % (host, port, db))

def process_line(line):
	left, comma, right = line.strip().partition(', ')
	if not left:
		return None
	if not comma:
		right = left
		left = "state_name"
	return left, right

with open(file, 'r') as f:
	for line in f:
		x = process_line(line)
		if x:
			if x[0] == "state_name":
				state_name = x[1]
			else:
				popularity = x[1]
				left, slash, alt = x[0].partition(' / ')
				cur = con.cursor()
				try:
					cur.execute("INSERT INTO common_streets VALUES(%s, %s, %s, %s)"
						, (state_name, left, popularity, alt)
						)
				finally:
					con.commit()

con.close()
del con

print('kthnxbai')
