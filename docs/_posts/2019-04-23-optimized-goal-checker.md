---
layout: post
title: Optimized Goal Checker
---

I wanted to start working on the motors to start controlling the players, but I have not really been satisified with the goal-checking mechanism (described in a [previous post]({% post_url 2019-03-16-basic-stats %})), because it depended too much on the performance of the webcam. In poor conditions, the camera records too few (useful) frames per seconds, which means that if you kick the ball very hard, there's a good chance that the camera won't catch it. This means that it will never detect the ball within the goal area (a precondition for detecting the goal), so a goal is never detected. 

## PIR Motion Sensor
First, I tried to use a PIR motion sensor. I wanted to place it near the goal area (outside the actual field), and if any motion is detected (i.e. when the ball is inside the goal), we infer that a goal is scored. However, it turned out to be too sensitive, because it also detected motion when the ball was moving between players (as it is visible through the goal). Again, I am no hardware expert, so it may have been obvious that it would not work. Anyway, I learned something. 

![PIR Motion Sensor]({{ site.baseurl }}/public/img/pirsensor.jpg)

## Webcam for motion detection
Instead, I figured I might be able to use *another* webcam, looking only at the goal. If motion is detected in the goal based on the camera feed, we infer that a goal is scored. I tried this and it turned out to actually work quite well.

![Goal cam]({{ site.baseurl }}/public/img/goalcam.jpg)

The implementation is based on [this blogpost](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/). The basic idea is to grab a frame as 'baseline', and then compare new frames to this. If there is a difference in pixels between the frames (and this difference is large enough), an object has been detected. In my case, this object would be the ball, and this means that a goal has been scored. 

<div>
    <img src="{{ site.baseurl }}/public/img/goalcam_raw.jpg" style="width: 48%; float: left" />
    <img src="{{ site.baseurl }}/public/img/goalcam_diff.png" style="width: 48%; float: left" />
</div>
<p style="clear: both;">The algorithm for detecting a goal is then:</p>

```
if motion detected and not goal_scored:
    if ball is not in field:
        goal_scored = True
else if ball is in field:
    goal_scored = False

if goal_scored:
    find scoring player using same method as before
```

See details of the implementation [here](https://github.com/andreasschmidtjensen/tablesoccer/commit/9d3e2ad38b210d218ea8d3682fbc39f262ab6ee4). In other words, the main difference is that we do not check if the ball suddenly disappears, but instead rely solely on the motion detection from the new camera. 

## Conclusion
With this addition, I feel that the resulting application is more useful, because it is more precise in goal detection. There are still some issues with poor lighting conditions and a wobbly setup for the main camera, but all in all, it works quite well. The main issue is really that I only had one spare webcam, so I am only able to detect goals in one end of the field! ... until I buy an extra, so it's not that big an issue.

Now I can't escape it anymore, so next big step will be to work on the motors and start controlling the players!