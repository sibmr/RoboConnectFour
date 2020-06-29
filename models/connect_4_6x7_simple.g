frame world 	{  }
frame connect4(world)   {}

# front / back
frame connect4_coll7(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 0.3 ]  pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-7.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll3(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 0.3 ]  pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-3.stl'     contact:-2  logical:{ } friction:.00001  }

# sides
frame connect4_coll4(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-4.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll5(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-5.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll6(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-6.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll8(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-8.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll9(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-9.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll2(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-2.stl'     contact:-2  logical:{ } friction:.00001  }
frame connect4_coll10(connect4) 	{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-10.stl'    contact:-2  logical:{ } friction:.00001  }
frame connect4_coll1(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-1.stl'     contact:-2  logical:{ } friction:.00001  }

# bottom
frame connect4_coll11(connect4) 	{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 -0.1 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-11.stl'    contact:-2  logical:{ } friction:.00001  }

## sphere for testing collision
#sphere2 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[-0.205,-0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#sphere3 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[-0.145,-0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#sphere4 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[-0.07, -0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#sphere5 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.00, -0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#sphere6 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.07, -0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#sphere7 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.14, -0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2} 
#sphere1 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.205,-0.05, 1.5, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
