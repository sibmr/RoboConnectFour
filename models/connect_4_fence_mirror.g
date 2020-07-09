## fences as boundries, viewing from infront of robots i.e. right arm is left
world {}
frame fence(world){}

#fence0 (fence){ shape:ssBox, Q:<t(-.95 0   .7)>, size:[.1 1.8 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## right, long fence
fence1 (fence){ shape:ssBox, Q:<t(0 -.95   .7)>, size:[1.8 .1 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## back
fence2 (fence){ shape:ssBox, Q:<t(0  .95   .7)>, size:[1.8 .1 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## front
fence3 (fence){ shape:ssBox, Q:<t(.95 .48  .7)>, size:[.1 .84 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## left front
fence4 (fence){ shape:ssBox, Q:<t(.95 -.48 .7)>, size:[.1 .84 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## left back

# mirror fences
fence5 (fence){ shape:ssBox, Q:<t(-.95 .48  .7)>, size:[.1 .84 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## right front
fence6 (fence){ shape:ssBox, Q:<t(-.95 -.48 .7)>, size:[.1 .84 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## right back

fence7 (fence){ shape:ssBox, Q:<t(.95 -.95 .725)>, size:[.1 .1 .15 .01], color:[.75 .125  .125], contact, logical:{ }, friction:.1 }  ## left back corner (red)
fence8 (fence){ shape:ssBox, Q:<t(.95  .95 .725)>, size:[.1 .1 .15 .01], color:[.75 .125  .125], contact, logical:{ }, friction:.1 }  ## left front corner (red)
fence9 (fence){ shape:ssBox, Q:<t(-.95 -.95 .725)>, size:[.1 .1 .15 .01], color:[.125 .125  .75], contact, logical:{ }, friction:.1 }  ## left back corner (blue)
fence10 (world){ shape:ssBox, Q:<t(-.95  .95 .725)>, size:[.1 .1 .15 .01], color:[.125 .125  .75], contact, logical:{ }, friction:.1 }  ## left front corner (blue)


slide (world){ shape:ssBox, pose=<T 0 0.5 0.65 0 0 -0.0499792 0.9987503 >, size:[1.8 0.9 .07 .01], color:[.3 .3  .3], contact, logical:{ }, friction:.1 }  ## ramp to keep spheres from escaping