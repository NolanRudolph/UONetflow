USE netflows;

CREATE TABLE segData0(
	startTime float,
	endTime float,
	srcIP varchar(16),
	dstIP varchar(16),
	IPProt int(3),
	srcPort int(5),
	dstPort int(5),
	TOSVal int(2),
	TCPFlags int(3),
	packets int(8),
	bytes int(8),
	routerInPort int(5),
	routerOutPort int(5),
	srcASN int(5),
	dstASN int(5)
)

LOAD DATA INFILE "segData0.csv"
INTO TABLE segData0
COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\n';
