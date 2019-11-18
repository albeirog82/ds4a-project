from random import seed
from random import randint

#create empty file to be writen to
file = open("neigh_data.csv", "w")
count = 0

seed(1)

#read original file
with open('neigh.geojson', 'r')as myfile:
	for line in myfile:
		
        #lines that don't need to be edited with an 'id'
		if not line.startswith('{"type":"Feature"'):
			file.write(line)
		else:
			pos=line.index('SCaCodigo')
			pos2=line.index('SHAPE_L')
			value = randint(0, 30)
			#print(line[pos:pos+100])
			#print(line[pos+12:pos+18])
			featureId = line[pos+12:pos+18]
			#print(line[pos+45:pos2-3])
			neigh_name = line[pos+45:pos2-3]
			count = count+1
			idNr = str(count)
			file.write(featureId + ','+ neigh_name + ',' + str(value) + "\n")

file.close()