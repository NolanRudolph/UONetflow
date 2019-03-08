import sys

try:
	F = open(sys.argv[1], "r")
	TERM = int(sys.argv[2])
except IndexError:
	print("Please issue as $ python " + sys.argv[0] + " [FILE] [TERM]")

for line in F:
	line = line.split(",")
	print(line[TERM])

