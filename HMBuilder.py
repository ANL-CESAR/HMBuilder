#!/usr/bin/python

import sys

n_radial = 10
n_axial = 100
n_azimuthal = 1

id = 100

uid = 1
tally_cells = []

n_tallies = 1000

def make_tallies():
	lines = []
	lines.append("""<?xml version="1.0"?>
<tallies>
<mesh id="1">
<type>rectangular</type>
<lower_left>-182.07 -182.07 -183.00</lower_left>
<upper_right>182.07  182.07  183.00</upper_right>
<dimension>1 1 100</dimension>
</mesh>

<tally id="1">
<filter type="mesh" bins="1" />
<filter>
<type>cell</type>
<bins>""")
	line = ''
	for i in range(0,len(tally_cells)):
		if i % 10 == 0 and i != 0:
			lines.append(line)
			line = str(tally_cells[i]) + ' '
		else:
			line = line + str(tally_cells[i]) + ' '
		if i > n_tallies:
			break
	
	lines.append("""
</bins>
</filter>
<scores> scatter absorption fission </scores>
<nuclides>U-234 U-235 U-236 U-238 Np-237 Pu-238 Pu-239 Pu-240 Pu-241 Pu-242 Am-241 Am-242m Am-243 Cm-242 Cm-244 Mo-95 Tc-99 Ru-101 Ru-103 Ag-109 Xe-135 Cs-133 Nd-143 Nd-145 Sm-147 Sm-149 Sm-150 Sm-151 Sm-152 Eu-153 Gd-155 O-16</nuclides>
</tally>
</tallies>""")	

	return lines
	

def make_pattern():
	lines = []
	for x in range(-2,19):
		lines.append([])
	uid = 1
	for x in range(-2,19):
		for y in range(-2,19):
			ok = 0
			if( x == 0 or x == 16 ):
				if( y >= 5 and y <= 11 ):
					ok = 1

			if( x == 1 or x == 15 ):
				if( y >= 3 and y <= 13 ):
					ok = 1

			if( x == 2 or x == 14 ):
				if( y >= 2 and y <= 14 ):
					ok = 1

			if( x == 3 or x == 4 or x == 13 or x == 12 ):
				if( y >= 1 and y <= 15 ):
					ok = 1

			if( x >= 5 and x <= 11 ):
				if( y >= 0 and y <= 16 ):
					ok = 1

			if( ok == 1 ):
				lines[x+2].append(str(uid))
				uid += 1
			else:
				lines[x+2].append('300')
	
	string = ''
	for x in range(0,21):
		for y in range(0,21):
			if( y != 0 ):
				string = string+' '
			string = string+lines[y][20-x].ljust(3)
		string = string+'\n'
				
	return string


def make_reactor():
	lines = []
	ll_x = -8 * 21.42;
	ll_y = -8 * 21.42;
	for x in range(0, 17):
		for y in range( 0, 17):
			ok = 0
			if( x == 0 or x == 16 ):
				if( y >= 5 and y <= 11 ):
					ok = 1

			if( x == 1 or x == 15 ):
				if( y >= 3 and y <= 13 ):
					ok = 1

			if( x == 2 or x == 14 ):
				if( y >= 2 and y <= 14 ):
					ok = 1

			if( x == 3 or x == 4 or x == 13 or x == 12 ):
				if( y >= 1 and y <= 15 ):
					ok = 1

			if( x >= 5 and x <= 11 ):
				if( y >= 0 and y <= 16 ):
					ok = 1

			if( ok == 1 ):
				#lines = lines + make_assembly( ll_x + x * 21.42, ll_y + y * 21.42 )
				lines = lines + make_assembly( 0, 0 )
	return lines

def is_guide_tube( x, y ):
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
		return 1
	else:
		return 0
	

def make_fuel_cell( c_x, c_y, x, y ):
	global tally_cells
	global id
	global n_radial
	lines = []
	x_coord = c_x + ( x - 8 ) * 1.26;
	y_coord = c_y + ( y - 8 ) * 1.26;

	start_id = id;

	# print surfaces
	for i in range(1, 11):
		radius = ( .41 / n_radial ) * i;
		lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' '+str(radius)+'"/>')
		id += 1

	id = start_id;

	# print cells
	lines.append('<cell id="'+str(id)+'" universe="'+str(uid)+'" material="1" surfaces="-'+str(id)+'"/>')
	tally_cells.append(id)
	for i in range(1, 10):
		lines.append('<cell id="'+str(id+1)+'" universe="'+str(uid)+'" material="1" surfaces="'+str(id)+' -'+str(id+1)+'"/>')
		id+=1
		tally_cells.append(id)
	id+=1

	#print cladding
	lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' .475"/>')
	lines.append('<cell id="'+str(id)+'" universe="'+str(uid)+'" material="2" surfaces="-'+str(id)+' '+str(id-1)+'"/>')
	id+=1

	
	# Make outer cell rectangular prism
	start_id = id
	l_x = x_coord - 0.63
	r_x = x_coord + 0.63
	l_y = y_coord - 0.63
	r_y = y_coord + 0.63
	top = 183
	bot = -183
	lines.append('<surface id="'+str(id)+'" type="x-plane" coeffs="'+str(l_x)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="x-plane" coeffs="'+str(r_x)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="y-plane" coeffs="'+str(l_y)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="y-plane" coeffs="'+str(r_y)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="z-plane" coeffs="'+str(bot)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="z-plane" coeffs="'+str(top)+'"/>')
	id+=1
	id = start_id
	lines.append('<cell id="'+str(id)+'" universe="'+str(uid)+'" material="3" surfaces="'+str(id)+' -'+str(id+1)+' '+str(id+2)+' -'+str(id+3)+' '+str(id+4)+' -'+str(id+5)+' '+str(id-1)+'"/>')
	id += 6
	
	return lines

def make_guide_cell( c_x, c_y, x, y ):
	global id
	lines = []
	start_id = id
	x_coord = c_x + ( x - 8 ) * 1.26
	y_coord = c_y + ( y - 8 ) * 1.26

	lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' .56"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="z-cylinder" coeffs="'+str(x_coord)+' '+str(y_coord)+' .62"/>')
	id = start_id

	lines.append('<cell id="'+str(id)+'" universe="'+str(uid)+'" material="3" surfaces="-'+str(id)+'"/>')
	id+=1
	lines.append('<cell id="'+str(id)+'" universe="'+str(uid)+'" material="2" surfaces="'+str(id-1)+' -'+str(id)+'"/>')
	id+=1
	
	# Make outer cell rectangular prism
	start_id = id
	l_x = x_coord - 0.63
	r_x = x_coord + 0.63
	l_y = y_coord - 0.63
	r_y = y_coord + 0.63
	top = 183
	bot = -183
	lines.append('<surface id="'+str(id)+'" type="x-plane" coeffs="'+str(l_x)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="x-plane" coeffs="'+str(r_x)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="y-plane" coeffs="'+str(l_y)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="y-plane" coeffs="'+str(r_y)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="z-plane" coeffs="'+str(bot)+'"/>')
	id+=1
	lines.append('<surface id="'+str(id)+'" type="z-plane" coeffs="'+str(top)+'"/>')
	id+=1
	id = start_id
	lines.append('<cell id="'+str(id)+'" universe="'+str(uid)+'" material="3" surfaces="'+str(id)+' -'+str(id+1)+' '+str(id+2)+' -'+str(id+3)+' '+str(id+4)+' -'+str(id+5)+' '+str(id-1)+'"/>')
	id += 6

	return lines
	

def make_assembly( c_x, c_y ):
	global id
	global uid
	lines = []
	for x in range(0, 17):
		for y in range(0, 17):
			if is_guide_tube(x,y):
				lines = lines + make_guide_cell(c_x, c_y, x, y)
			else:
				lines = lines + make_fuel_cell( c_x, c_y, x, y)
	uid += 1

	return lines
		
if( len(sys.argv) != 2 ):
	n_tallies = 2000000000
	print "Printing full geometry and ALL tallies..."
else:
	n_tallies = int(sys.argv[1])
	print "Printing full geometry and "+sys.argv[1]+" tallies..."

lines = []
lines.append('<?xml version="1.0"?>')
lines.append('<geometry>')
lines.append('<cell id="1"  fill="1129908" surfaces=" -6 34 -36" />')
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
<!-- cell for water assembly (hot) -->
<cell id="70" universe="300" material="3" surfaces="34 -36" />

<!-- Fuel Assembly and Water Stuffs -->""")
#<cell id="1"  fill="200"    surfaces="  -6 34 -35" /> <!-- Lower core -->
#<cell id="2"  fill="201"    surfaces="  -6 35 -36" /> <!-- Upper core -->

lines = lines + make_reactor()
  
lines.append('<lattice id="'+str(id)+'">')
lines.append("""
<type>rectangular</type>
<dimension>21 21</dimension>
<lower_left>-224.91 -224.91</lower_left>
<width>21.42 21.42</width>
<universes>""")
lines.append(make_pattern())
lines.append("""
</universes>
</lattice>""")

lines.append('</geometry>')

fp = open("geometry.xml", "w")
for line in lines:
	print >> fp, line
fp.close()

lines = make_tallies()	
fp = open("tallies.xml", "w")
for line in lines:
	print >> fp, line
fp.close()
