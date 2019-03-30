---
layout: post
title: Connecting to Hardware
---

I have mentioned before that I have absolutely no experience in working with hardware, so I have decided to use [Arduino](https://www.arduino.cc/) to get something up and running fairly quickly. 

Using an Arduino board, it is possible to interact with all sorts of hardware components through a serial interface. The board is programmed using the Arduino language, which is just a set of C/C++ functions, that are being called in the `setup()` and `loop()` functions of an application. The names of these functions make their purpose pretty clear. 

I ordered a [Starter Kit](https://www.elegoo.com/product/elegoo-uno-project-super-starter-kit/) which includes the Arduino board itself, a lot of components to get started and a pretty good tutorial. After completing the first few tutorials (connecting LEDs and making them blink), I wanted to connect to the Table Soccer application.

## Connecting to Python
As mentioned, the Arduino connects to a computer through a serial interface. This makes it pretty straightforward to communicate with it through Python. I used the [pySerial](https://github.com/pyserial/pyserial) library to access the serial port. It is very simple to use. For example, to send a string to the Arduino, the following code does the job:

```
import serial
s = serial.Serial("COM3", 9600)
s.write(b'Hello world!')
```

We connect to `COM3` (as found in the device manager: <img src="{{ site.baseurl }}/public/img/comport_device_manager.png" style="display: inline; margin: 0;" />) and specify a baud rate of 9600[^1]. Reading the data on the Arduino is also easy enough:

```
void setup() {
  Serial.begin(9600);
  // initialize components
}

void loop() {
  while (Serial.available() > 0) {
    c = Serial.read();
    // do something with c
  }
}
```

## Small steps, but steps nonetheless
At some point, I will need to connect to some kind of motors that can control the players. To do so, I also need to attach the motors to the board. Since I am still new to Arduino, I wanted to try something simpler first, so I used an LCD and a buzzer to announce the goals of a match. 

Using the very nice tutorial that came with the board, I was able to quickly setup an LCD that can write the scores. I also added a buzzer to play a sound when a goal is scored. The final schematics are as follows:

![Arduino Schematics]({{ site.baseurl }}/public/img/schematics_1_lcd+buzzer_bb.png)

From the application, I can then send commands to the board through the serial port. It is done simply by sending strings, where the first character indicates the type of message and the rest of the string is the content. To write a message on the display, we can send the command `Dtext` and to play a sound, we use e.g. `SA`, where A is 'away', so we can play different sounds for each team. The implementation is found in [this commit](https://github.com/andreasschmidtjensen/tablesoccer/commit/c4e473cad15ae9f2042cf38acf0c8935a5c163a0).

The result is then the following - extremely pretty - scoreboard:

![Scoreboard]({{ site.baseurl }}/public/img/scoreboard.jpg)

## Next steps
I have previously heard that Arduino makes it very easy to prototype, but I was surprised at how easy it was to have something working. Not just as a standalone application, but something that actually connects with the rest of the Table Soccer application! 

Next, I will have to look into adding motors to the system now to get those players moving. 

### Footnotes
[^1]: The baud rate specifies the number of bits per second that can be transmitted through the channel. 

