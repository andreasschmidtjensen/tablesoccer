---
layout: post
title: Poor man's tracking device
---

In Table Soccer, the balls often travel at very high speed, so in order to capture this, I would need more than just a regular webcam. I did however say that one of the goals is to let it play with my kids. Also, I'm currently not ready to spend large sums on high-speed camera just for my hobby project.

The first solution is therefore to use a camera I bought previously. If this proves to perform too bad, I will consider buying something better. My camera goes by the great name 'Creative Live! Cam Chat HD' and is able to record 720p at 30 FPS. 

<p align="center">
    <img src="{{ site.baseurl }}/public/img/creative-live-cam-chat-hd.jpg" />
</p>

I will not break any speed records using it, but I hope that it can get the job done. 

## The all-seeing eye

The camera needs to be placed above the playing field at a height that allows it to see everything. There are probably many ways to achieve this, but I wanted something that is built into the game, so that if the table is moved, the camera doesn't need to be re-adjusted. 

I first considered building a structure out of wood, that could be put on top and in which the camera could be placed, but to keep costs down (and to get some progress!), I found a much cheaper and faster solution: Galvanised steel wire. It is a metal wire, that can be bent but is still able to carry the small weight of the camera. 

![Setup overview]({{ site.baseurl }}/public/img/setup-sketch.png)

As may be visible from the pretty bad sketch above, I used four tiny screws to fixate the wire at each corner of the table. The camera is put on top of the construction and is kept in position by putting wire around it.

![Final setup]({{ site.baseurl }}/public/img/setup-result.jpg)

The final result is really as advertised: A poor man's tracking device. The structure is much more stable than I had hoped for, but it is easy to inadvertently move the camera, e.g. when adjusting the cord or moving the table.

## The view from above

In the end, the resulting view is - at this early stage - acceptable:

![View from above]({{ site.baseurl }}/public/img/view-from-above.jpg)

 From this, I can start producing training data for the YOLO model. It remains to be seen whether the performance is good enough. Some may be solvable simply by adding more light to the scene, but as mentioned, it is very possible that I have to get a better camera!

