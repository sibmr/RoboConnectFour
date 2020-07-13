#frame world 	{  }
#frame connect4(world)   {}
#
## front / back
#frame connect4_coll7(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 0.3 ]  pose=<T 0  0.005 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-7.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll3(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 0.3 ]  pose=<T 0 -0.005 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-3.stl'     contact:-2  logical:{ } friction:.00001  }
#
## sides
#frame connect4_coll4(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-4.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll5(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-5.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll6(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-6.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll8(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-8.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll9(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-9.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll2(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-2.stl'     contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll10(connect4) 	{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-10.stl'    contact:-2  logical:{ } friction:.00001  }
#frame connect4_coll1(connect4) 		{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-1.stl'     contact:-2  logical:{ } friction:.00001  }
#
## bottom
#frame connect4_coll11(connect4) 	{  shape:mesh  color:[ 0.9 0.9 0.9 1 ]    pose=<T 0 0 0.65 0 0 0 1 > meshscale=0.001 mesh:'meshes/simple_model/Connect4-6X7-simple-11.stl'    contact:-2  logical:{ } friction:.00001  }

## sphere for testing collision
#spherea6 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[-0.205,-0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#spherea5 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[-0.137,-0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#spherea4 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[-0.07, -0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#spherea3 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.00, -0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#spherea2 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.07, -0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}
#spherea1 		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.137, -0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2} 
#spherea0		{  shape:sphere, size:[0.026],, mass:0.2 X:<[ 0.205,-0.05, 1.2, 0, 0, 0, 1]> color:[ 1 0 0 1 ] friction:.2}

spherea00		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.205 ,-0.05, .70, 0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea01		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.205 ,-0.05, .77, 0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea02		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.205 ,-0.05, .84, 0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea03		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.205 ,-0.05, .91, 0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea04		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.205 ,-0.05, .98, 0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea05		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.205 ,-0.05,1.05, 0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea10		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.1375,-0.05,  .70,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea11		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.1375,-0.05,  .77,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea12		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.1375,-0.05,  .84, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea13		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.1375,-0.05,  .91, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea14		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.1375,-0.05,  .98, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea15		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.1375,-0.05, 1.05, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
spherea20 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.07,  -0.05,  .70,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea21 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.07,  -0.05,  .77,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea22 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.07,  -0.05,  .84, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea23 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.07,  -0.05,  .91, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea24 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.07,  -0.05,  .98, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea25 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.07,  -0.05, 1.05, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea30 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.00,  -0.05,  .70,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea31 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.00,  -0.05,  .77,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea32 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.00,  -0.05,  .84, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea33 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.00,  -0.05,  .91, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea34		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.00,  -0.05,  .98, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea35 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[ 0.00,  -0.05, 1.05, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
spherea40 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.07,  -0.05,  .70,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea41		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.07,  -0.05,  .77,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea42 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.07,  -0.05,  .84, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea43 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.07,  -0.05,  .91, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea44 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.07,  -0.05,  .98, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea45 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.07,  -0.05, 1.05, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea50 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.1375,-0.05,  .70,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea51 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.1375,-0.05,  .77,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
#spherea52 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.1375,-0.05,  .84, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea53 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.1375,-0.05,  .91, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea54 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.1375,-0.05,  .98, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea55 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.1375,-0.05, 1.05, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
spherea60 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.205, -0.05,  .70,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea61 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.205, -0.05,  .77,0, 0, 0, 1]>    color:[ 0 0 1 1 ] friction:.2}
spherea62 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.205, -0.05,  .84, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea63 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.205, -0.05,  .91, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea64 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.205, -0.05,  .98, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}
#spherea65 		{  shape:sphere, size:[0.027],, mass:0.2 X:<[-0.205, -0.05, 1.05, 0, 0, 0, 1]>   color:[ 0 0 1 1 ] friction:.2}