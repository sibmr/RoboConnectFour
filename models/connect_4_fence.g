## fences as boundries, viewing from infront of robots i.e. right arm is left
world {}

fence (world){ shape:ssBox, Q:<t(-.95 0   .7)>, size:[.1 1.8 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## right, long fence
fence (world){ shape:ssBox, Q:<t(0 -.95   .7)>, size:[1.8 .1 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## back
fence (world){ shape:ssBox, Q:<t(0  .95   .7)>, size:[1.8 .1 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## front
fence (world){ shape:ssBox, Q:<t(.95 .48  .7)>, size:[.1 .84 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## left front
fence (world){ shape:ssBox, Q:<t(.95 -.48 .7)>, size:[.1 .84 .1 .005], color:[.3 .3 .3], contact, logical:{ }, friction:.1 }  ## left back

fence (world){ shape:ssBox, Q:<t(.95 -.95 .725)>, size:[.1 .1 .15 .01], color:[.75 .125  .125], contact, logical:{ }, friction:.1 }  ## left back corner (red)
fence (world){ shape:ssBox, Q:<t(.95  .95 .725)>, size:[.1 .1 .15 .01], color:[.75 .125  .125], contact, logical:{ }, friction:.1 }  ## left front corner (red)
fence (world){ shape:ssBox, Q:<t(-.95 -.95 .725)>, size:[.1 .1 .15 .01], color:[.125 .125  .75], contact, logical:{ }, friction:.1 }  ## left back corner (blue)
fence (world){ shape:ssBox, Q:<t(-.95  .95 .725)>, size:[.1 .1 .15 .01], color:[.125 .125  .75], contact, logical:{ }, friction:.1 }  ## left front corner (blue)