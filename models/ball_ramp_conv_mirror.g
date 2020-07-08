frame world 	{  }
frame ball_ramp1(world)   {}
frame ball_ramp2(world)   {}

frame ball_ramp (ball_ramp1)	{shape:mesh  pose=<T 0.9 0.0 0.66 0.7071 0 0 0.7071 > meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv1.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp1)	{shape:mesh  pose=<T 0.9 0.0 0.66 0.7071 0 0 0.7071 > meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv2.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp1)	{shape:mesh  pose=<T 0.9 0.0 0.66 0.7071 0 0 0.7071 > meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv3.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp1)	{shape:mesh  pose=<T 0.9 0.0 0.66 0.7071 0 0 0.7071 > meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv4.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp1)	{shape:mesh  pose=<T 0.9 0.0 0.66 0.7071 0 0 0.7071 > meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv5.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}

frame ball_ramp (ball_ramp2)	{shape:mesh  pose=<T -0.9 0.0 0.66 0.7071 0 0 -0.7071> meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv1.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp2)	{shape:mesh  pose=<T -0.9 0.0 0.66 0.7071 0 0 -0.7071> meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv2.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp2)	{shape:mesh  pose=<T -0.9 0.0 0.66 0.7071 0 0 -0.7071> meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv3.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp2)	{shape:mesh  pose=<T -0.9 0.0 0.66 0.7071 0 0 -0.7071> meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv4.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
frame ball_ramp (ball_ramp2)	{shape:mesh  pose=<T -0.9 0.0 0.66 0.7071 0 0 -0.7071> meshscale=0.05 color:[ 0.9 0.9 0.9 1 ]  mesh:'meshes/ball_ramp-convex/ball_ramp_conv5.stl' visual, contact:1, rel_includes_mesh_center contact, logical:{ } friction:.00001}
