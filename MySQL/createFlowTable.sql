CREATE TABLE segData(
	startTime double,
	endTime double,
	srcIP varchar(16),
	dstIP varchar(16),
	srcPort varchar(5),
	dstPort varchar(5),
	IPProt varchar(3),
	TOSVal varchar(2),
	TCPFlags varchar(3),
	packets int(8),
	bytes int(8),
	routerInPort varchar(5),
	routerOutPort varchar(5),
	srcASN varchar(5),
	dstASN varchar(5)
);
