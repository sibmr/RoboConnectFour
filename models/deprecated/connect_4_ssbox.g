frame world 	{  }
frame connect4(world)   {X:<[0,  0,  1, 0, 0, 0, 1]>}
## this should be the visible model - still uses its collisions when uncommented
##frame connect4_vis(connect4) 		{  shape:ssBox                          pose=<T 0 0 0.65 0 0 0 1 > size:[ 0.9 0.9 0.9 ] color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/Connect4-6X7_visible.ply' visual  }
##frame connect4_vis(connect4) 		{  shape:ssBox                          pose=<T 0 0 0.65 0 0 0 1 > size:[ 0.9 0.9 0.9 ] color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/Connect4-6X7_visible.ply' visual  }
##frame connect4_vis(connect4) 		{  shape:ssBox                          pose=<T 0 0 0.65 0 0 0 1 > size:[ 0.9 0.9 0.9 ] color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/Connect4-6X7_visible.ply' visual  }
obj0(connect4) 	{  shape:ssBox, size:[0.6, 0.02, 0.5, 0.01],color:[ 0 0 1 0.1 ], mass:0.2 X:<[0,  0.02,  0, 0, 0, 0, 1]>}
obj1(connect4) 	{  shape:ssBox, size:[0.6, 0.02, 0.5, 0.01],color:[ 0 0 1 0.1 ], mass:0.2 X:<[0, -0.02,  0, 0, 0, 0, 1]> }
## these are the approximate convex collision shapes for the model 
## frame connect4_coll1(connect4) 		{  shape:mesh  color:[ 0.8 0.2 0.2 1 ]  pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/Connect4-6X7-convex/Connect4-6X7_hull_1.stl'   noVisual, contact:-2  logical:{ } friction:.001  }

## sphere for testing collision
sphere2 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[-0.20, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}
sphere3 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[-0.14, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}
sphere4 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[-0.07, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}
sphere5 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[ 0.00, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}
sphere6 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[ 0.07, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}
sphere7 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[ 0.14, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]} 
sphere1 		{  shape:sphere, size:[0.022],, mass:0.2 X:<[ 0.20, 0, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ]}