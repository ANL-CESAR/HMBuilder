==============================================================================
 ____  ____  ____    ____  ______             _   __        __                
|_   ||   _||_   \  /   _||_   _ \           (_) [  |      |  ]               
  | |__| |    |   \/   |    | |_) | __   _   __   | |  .--.| | .---.  _ .--.  
  |  __  |    | |\  /| |    |  __'.[  | | | [  |  | |/ /'`\' |/ /__\\[ `/'`\] 
 _| |  | |_  _| |_\/_| |_  _| |__) || \_/ |, | |  | || \__/  || \__., | |     
|____||____||_____||_____||_______/ '.__.'_/[___][___]'.__.;__]'.__.'[___]    

==============================================================================
Contact Information
==============================================================================

Organization:     Center for Exascale Simulation of Advanced Reactors (CESAR)
                  Argonne National Laboratory

Development Lead: John Tramm <jtramm@mcs.anl.gov>

==============================================================================
What is HMBuilder?
==============================================================================

The goal of the HMBuilder script is to simulate the Hoogenboom-Martin
reactor with separate tally bins for 10 concentric radial regions and
100 axial cuts for each fuel rod.

HMBuilder is an input deck creator for OpenMC, capabel of creating the
input files necessary to define the Hoogenboom-Martin TB model.

When run, the following files are created in the current working
directory. Note that the files are fairly large (~338MB total).

->    geometry.xml
->    tallies.xml

The geometry.xml file defines 636,240 infinite cylinder cells representing
all of the 10 radial regions of each fuel cell.

The tallies.xml file defines a mesh covering the entire reactor zone,
with 100 regions along the z-axis, as well as specifying each of the
636,240 cells as separate tallies. This results in a grand total of
63,624,000 tally spaces.

Considering approximately 33 fuel nuclides, each with 6 reaction types, and
the size of a tally object being 24 bytes, the total tally data can be
calculated as:

	Tally Data = 63,624,000 tallies x 24 bytes/tally x 33 nucs x 3 XS's
	           = 140.8 GB
	           = 0.14  TB

==============================================================================
Quick Start Guide
==============================================================================

Download----------------------------------------------------------------------

	Download of the TB_tallyserver source files are available from our
	github repository (https://github.com/jtramm/TB_tallyerver).

	The repository can be downloaded with the following command:
	
	>$ git clone git://github.com/jtramm/TB_tallyerver.git	

	To begin use of the code, you will have to navigate to
	the src directory:

	>$ cd TB_tallyserver

Running HMBuilder--------------------------------------------------------

	To run HMBuilder with default settings, use the following command:

	>$ ./HMBuilder

	This program is also capabale of generating smaller models, representing
	a smaller portion of the total number of fuel assemblies in the reactor.
	This feature may be useful for testing purposes. The script needs to
	be altered manually for this though, changing the 'n_tallies' value.

==============================================================================
Theoretical Basis
==============================================================================

This basis for this reactor model, including specifications for the
geometry, material selection, and nuclide distribution, is specified in
the Hoogenboom-Martin reactor model, as described in the paper below:

J.E. Hoogenboom, W.R. Martin, B. Petrovic, “The Monte Carlo performance
benchmark test aims, specifications and first results,” International
Conference on Mathematics and Computational Methods Applied to Nuclear
Science and Engineering, Rio de Janeiro, Brazil (2011).

Constant annual rings can be computed as:

Ri = sqrt( Rn^2 * i / n )

For n rings, where Rn is the outer (nth) Radius, and Ri is the radius in question.
