frame world 	{  }
frame connect4(world) 	{  shape:mesh  pose=<T 0 0 0.8 0 0 0 1 > meshscale=0.001 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/connect4_10x30x50_ascii_medq.stl' visual, contact:-2, rel_includes_mesh_center  
			contact, logical:{ }
    			friction:.001

			}
sphere1 		{  shape:sphere, size:[0.02],, mass:0.2 X:<[0.07, 0, 1, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}
