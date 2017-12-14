import urllib2
import errno
import os
from datetime import datetime
import json
import tablib

data = {}
completedList = ['2017-10-28', '2017-11-01', '2017-10-26', '2017-10-30', '2017-10-31', '2017-10-29', '2017-10-27', '2017-11-02', '2017-11-03', '2017-11-04', '2017-11-05']
def read(id, filename):
	mydir = os.path.join(os.getcwd(), 'files')
	try:
		os.makedirs(mydir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	
	with open(os.path.join(mydir, filename)) as data_file:
		string = data_file.read()
		string = unicode(string, "utf-8")
		results = json.loads(string)

		for result in results:
			date = result.get('Date', '')
			dateList = date.split(" ")
			date = dateList[0]
			if date in completedList:
				continue

			if date not in data:
					data[date] = {}
			for res in result.get('Data', []):
				CommodityName = res.get('CommodityNameE', '')
				if CommodityName not in data[date]:
					data[date][CommodityName] = []
				data[date][CommodityName].append({
					'Hrate': float(res.get('Hrate', 0)),
					'Mrate': float(res.get('Mrate', 0)),
					'Lrate': float(res.get('Lrate', 0)),
					'Variety': res.get('VarietyE', ''),
					'Unit': res.get('UnitE', ''),
					'Name': res.get('ApmcNameE', ''),
					'Quantity': res.get('Quantity', ''),
					'id': str(id)
				})
	return data

"""
def save(data, filename):
	mydir = os.path.join(os.getcwd(), 'files',datetime.now().strftime('%Y%m%d'))
	print mydir
	try:
		os.makedirs(mydir)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	with open(os.path.join(mydir, filename), 'wb') as d:
		d.write(data)
		print "Done %s" % (filename)
"""
marktetids = ["086","007","184","209","147","047","001","010","030","127","061","012","01201","111","080","087","046","04601","027","163","035","217","004","210","21001","048","258","245","134","262","074","149","308","251","231","187","261","039","03901","118","065","028","252","025","119","121","286","298","148","059","006","014","084","15601","023","159","293","280","013","092","113","174","109","285","235","154","257","250","038","075","07501","101","296","016","08101","01601","291","009","00901","089","100","10001","213","157","076","033","03303","03302","03301","204","282","263","053","102","294","175","105","077","107","264","182","082","06701","179","192","002","00201","00202","091","167","275","171","246","247","015","01501","01502","108","005","00501","069","122","236","037","024","274","083","068","265","172","130","219","066","220","183","114","238","224","195","050","05002","05003","135","205","254","034","307","036","155","225","228","040","266","011","01101","144","093","09301","018","064","06401","056","216","136","278","240","029","043","021","110","142","152","268","112","055","044","132","106","09601","096","299","270","022","02204","02205","02202","290","042","04201","255","241","267","052","104","116","133","303","115","145","272","017","060","01701","070","22901","090","168","259","088","211","020","230","098","09801","099","161","095","09501","071","07101","271","27101","232","041","309","003","215","146","164","117","248","125","073","139","058","197","242","24201","302","097","169","292","170","177","085","126","12001","138","165","063","049","04901","153","008","019","284"]
"""
URL = 'http://www.msamb.com/ApmcDetail/DataGridBind?commodityCode=null&apmcCode=%s'
for market_id in marktetids:
	response = urllib2.urlopen(URL % (market_id))
	data = response.read()
	save(data, market_id)
"""

for market_id in marktetids:
	read(market_id, '20171106/' + market_id)


headers = ('COMMODITY', 'APMC', 'UNIT', 'QUANTITY', 'LRATE', 'MRATE', 'HRATE', 'VARIETY', 'APMC ID')
book = tablib.Databook()
for date in data:
	print date
	rates = tablib.Dataset(headers=headers, title=date)
	for CommodityName in data[date]:
		for index, res in enumerate(data[date][CommodityName]):
			
			if index == 0:
				col_data = (CommodityName, res.get('Name', ''), res.get('Unit', ''), res.get('Quantity', ''), res.get('Lrate', ''), res.get('Mrate', ''), res.get('Hrate', ''), res.get('Variety', ''), res.get('id', ''))
			else:
				col_data = ('', res.get('Name', ''), res.get('Unit', ''), res.get('Quantity', ''), res.get('Lrate', ''), res.get('Mrate', ''), res.get('Hrate', ''), res.get('Variety', ''), res.get('id', ''))
			
			rates.append(col_data)
	
	book.add_sheet(rates)			
			#print index
			#print res
with open('output.xls', 'wb') as f:
    f.write(book.xls)
"""

john = ('John', 'Adams', 90)
george = ('George', 'Washington', 67)
tom = ('Thomas', 'Jefferson', 50)


#founders.append(john)
#founders.append(george)
#founders.append(tom)
with open('output.xls', 'wb') as f:
    f.write(rates.xls)
"""