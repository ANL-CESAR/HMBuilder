#!/usr/bin/python

id = 100

def make_assembly( c_x, c_y ):
	global id
	lines = []
	for x in range(1, 18):
		for y in range(1, 18):
			# if guide tube
			if(
					(x==2 and (y==5 or y==8 or y==11))
					 or 
					(x==3 and (y==3 or y==13))
					 or 
					(x==5 and (y==2 or y==5 or y==8 or y==11 or y==14))
					 or 
					(x==8 and (y==2 or y==5 or y==8 or y==11 or y==14))
					 or 
					(x==11 and (y==2 or y==5 or y==8 or y==11 or y==14))
					 or 
					(x==13 and (y==3 or y==13))
					 or 
					(x==14 and (y==5 or y==8 or y==11))
			  ):
				start_id = id;
				x_coord = c_x + ( x - 8 ) * 1.26;
				y_coord = c_y + ( y - 8 ) * 1.26;
				#Water
				lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' .56">')
				id+=1
				#Cladding
				lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' .62">')
				id = start_id
				lines.append('<cell id = "'+str(id)+'" material="3" surfaces="-'+str(id)+'"/>')
				id+=1
				lines.append('<cell id = "'+str(id)+'" material="3" surfaces="-'+str(id)+'"/>')
				id+=1
			else:
				x_coord = c_x + ( x - 8 ) * 1.26;
				y_coord = c_y + ( y - 8 ) * 1.26;

				start_id = id;

				# print surfaces
				for i in range(1, 11):
					radius = ( .41 / 10.0 ) * i;
					lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' '+str(radius)+'"/>')
					id += 1

				id = start_id;

				# print cells
				lines.append('<cell id = "'+str(id)+'" material="1" surfaces="-'+str(id)+'"/>')
				for i in range(1, 10):
					lines.append('<cell id ="'+str(id+1)+'" material="1" surfaces="'+str(id)+' '+str(id+1)+'"/>')
					id+=1;

	return lines
		
lines = []
lines.append('<?xml version="1.0"?>')
lines.append('<geometry>')
lines.append("""
<!-- All Basic Reactor Part Surfaces -->
<surface id="5" type="z-cylinder" coeffs="0. 0. 187.6" />
<surface id="6" type="z-cylinder" coeffs="0. 0. 209.0" />
<surface id="7" type="z-cylinder" coeffs="0. 0. 229.0" />
<surface id="8" type="z-cylinder" coeffs="0. 0. 249.0" boundary="vacuum" />
<surface id="31" type="z-plane" coeffs="-229.0" boundary="vacuum" />
<surface id="32" type="z-plane" coeffs="-199.0" />
<surface id="33" type="z-plane" coeffs="-193.0" />
<surface id="34" type="z-plane" coeffs="-183.0" />
<surface id="35" type="z-plane" coeffs="0.0" />
<surface id="36" type="z-plane" coeffs="183.0" />
<surface id="37" type="z-plane" coeffs="203.0" />
<surface id="38" type="z-plane" coeffs="215.0" />
<surface id="39" type="z-plane" coeffs="223.0" boundary="vacuum" />

<!-- All Basic Reactor Part Cells -->
<cell id="1"  fill="200"    surfaces="  -6 34 -35" /> <!-- Lower core -->
<cell id="2"  fill="201"    surfaces="  -6 35 -36" /> <!-- Upper core -->
<cell id="3"  material="8"  surfaces="  -7 31 -32" /> <!-- Lower core plate region -->
<cell id="4"  material="9"  surfaces="  -5 32 -33" /> <!-- Bottom nozzle region -->
<cell id="5"  material="12" surfaces="  -5 33 -34" /> <!-- Bottom FA region -->
<cell id="6"  material="11" surfaces="  -5 36 -37" /> <!-- Top FA region -->
<cell id="7"  material="10" surfaces="  -5 37 -38" /> <!-- Top nozzle region -->
<cell id="8"  material="7"  surfaces="  -7 38 -39" /> <!-- Upper plate region -->
<cell id="9"  material="3"  surfaces="6 -7 32 -38" /> <!-- Downcomer -->
<cell id="10" material="5"  surfaces="7 -8 31 -39" /> <!-- RPV -->
<cell id="11" material="6"  surfaces="5 -6 32 -34" /> <!-- Bottom of radial reflector -->
<cell id="12" material="7"  surfaces="5 -6 36 -38" /> <!-- Top of radial reflector -->

<!-- Fuel Assembly and Water Stuffs -->""")

lines = lines + make_assembly(0,0)

for line in lines:
	print line
