# Little Interactions Everywhere

Alan Hsieh (amh425) - Developed scripting code to MQTT device integration.

Tsung-Yin Hsieh (th542) - Ideated design for visualizer interface and co-developed sketches for protyping and interaction.

Yi-Ru Pei (yp329) - Co-developed sketches for prototyping and interaction, developed user need and hospital experience for product ideation.

Jonathan Tan (jmt362) - Using Django writing visualizer for web browser interface.

Henry Wu (hw574) - Data management using PostgreSQL to manage MQTT data storage.  Co-developed scripting code for MQTT.

## Prep

1. Pull the new changes from the class interactive-lab-hub. (You should be familiar with this already!)
2. Install [MQTT Explorer](http://mqtt-explorer.com/) on your laptop. If you are using Mac, MQTT Explorer only works when installed from the [App Store](https://apps.apple.com/app/apple-store/id1455214828).
3. Readings before class:
   * [MQTT](#MQTT)
   * [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) and [video](https://vimeo.com/15932020)


## Overview

The point of this lab is to introduce you to distributed interaction. We have included some Natural Language Processing (NLP) and Generation (NLG) but those are not really the emphasis. Feel free to dig into the examples and play around the code which you can integrate into your projects if wanted. However, we want to emphasize that the grading will focus on your ability to develop interesting uses for messaging across distributed devices. Here are the four sections of the lab activity:

A) [MQTT](#part-a)

B) [Send and Receive on your Pi](#part-b)

C) [Streaming a Sensor](#part-c)

D) [The One True ColorNet](#part-d)

E) [Make It Your Own](#part-)

## Part 1.

### Part A
### MQTT

MQTT is a lightweight messaging portal invented in 1999 for low bandwidth networks. It was later adopted as a defacto standard for a variety of [Internet of Things (IoT)](https://en.wikipedia.org/wiki/Internet_of_things) devices. 

#### The Bits

* **Broker** - The central server node that receives all messages and sends them out to the interested clients. Our broker is hosted on the far lab server (Thanks David!) at `farlab.infosci.cornell.edu/8883`. Imagine that the Broker is the messaging center!
* **Client** - A device that subscribes or publishes information to/on the network.
* **Topic** - The location data gets published to. These are *hierarchical with subtopics*. For example, If you were making a network of IoT smart bulbs this might look like `home/livingroom/sidelamp/light_status` and `home/livingroom/sidelamp/voltage`. With this setup, the info/updates of the sidelamp's `light_status` and `voltage` will be store in the subtopics. Because we use this broker for a variety of projects you have access to read, write and create subtopics of `IDD`. This means `IDD/ilan/is/a/goof` is a valid topic you can send data messages to.
*  **Subscribe** - This is a way of telling the client to pay attention to messages the broker sends out on the topic. You can subscribe to a specific topic or subtopics. You can also unsubscribe. Following the previouse example of home IoT smart bulbs, subscribing to `home/livingroom/sidelamp/#` would give you message updates to both the light_status and the voltage.
* **Publish** - This is a way of sending messages to a topic. Again, with the previouse example, you can set up your IoT smart bulbs to publish info/updates to the topic or subtopic. Also, note that you can publish to topics you do not subscribe to. 


**Important note:** With the broker we set up for the class, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`. Also, setting up a broker is not much work, but for the purposes of this class, you should all use the broker we have set up for you!


#### Useful Tooling

Debugging and visualizing what's happening on your MQTT broker can be helpful. We like [MQTT Explorer](http://mqtt-explorer.com/). You can connect by putting in the settings from the image below.


![input settings](imgs/mqtt_explorer.png?raw=true)


Once connected, you should be able to see all the messages under the IDD topic. , go to the **Publish** tab and try publish something! From the interface you can send and plot messages as well. Remember, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`.


<img width="1026" alt="Screen Shot 2022-10-30 at 10 40 32 AM" src="https://user-images.githubusercontent.com/24699361/198885090-356f4af0-4706-4fb1-870f-41c15e030aba.png">



### Part B
### Send and Receive on your Pi

[sender.py](./sender.py) and and [reader.py](./reader.py) show you the basics of using the mqtt in python. Let's spend a few minutes running these and seeing how messages are transferred and shown up. Before working on your Pi, keep the connection of `farlab.infosci.cornell.edu/8883` with MQTT Explorer running on your laptop.

**Running Examples on Pi**

* Install the packages from `requirements.txt` under a virtual environment, we will continue to use the `circuitpython` environment we setup earlier this semester:

  ```
  pi@raspberrypi:~/Interactive-Lab-Hub $ source circuitpython/bin/activate
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub $ cd Lab\ 6
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ pip install -r requirements.txt
  ...
  ```
* Run `sender.py`, fill in a topic name (should start with `IDD/`), then start sending messages. You should be able to see them on MQTT Explorer.

  ```
  (circuitpython) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python sender.py
  >> topic: IDD/AlexandraTesting
  now writing to topic IDD/AlexandraTesting
  type new-topic to swich topics
  >> message: testtesttest
  ...
  ```
* Run `reader.py`, and you should see any messages being published to `IDD/` subtopics. Type a message inside MQTT explorer and see if you can receive it with `reader.py`.

  ```
  (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python reader.py
  ...
  ```

<img width="890" alt="Screen Shot 2022-10-30 at 10 47 52 AM" src="https://user-images.githubusercontent.com/24699361/198885135-a1d38d17-a78f-4bb2-91c7-17d014c3a0bd.png">


**\*\*\*Consider how you might use this messaging system on interactive devices, and draw/write down 5 ideas here.\*\*\***

1. We design a covid 19 application to detect whether people have been exposed to covid infected people and use IoT to prevent cluster infection
![p1](imgs/L6p1.jpg)

2. Use IoT sensors to measure water humidity to know if plants need to be watered
![p2](imgs/L6p2.jpg)

3. We use captive sensors to detect and inform patients which Department they are going to work in.
![p3](imgs/L6p3.jpg)

4. We design the Traffic flow sensor by using the MQTT explorer to detect the traffic jam situation. To, adjust the traffic light to control the traffic flow in a specific line.
![p4](imgs/L6p4.jpg)

5. We use sensors to automatically detect the brightness of the room and automatically adjust the brightness of the room at different times of the day
![p5](imgs/L6p5.jpg)


### Part C
### Streaming a Sensor

We have included an updated example from [lab 4](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Fall2021/Lab%204) that streams the [capacitor sensor](https://learn.adafruit.com/adafruit-mpr121-gator) inputs over MQTT. We will also be running this example under `circuitpython` virtual environment.

Plug in the capacitive sensor board with the Qwiic connector. Use the alligator clips to connect a Twizzler (or any other things you used back in Lab 4) and run the example script:

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
<img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150"/>
<img src="https://media.discordapp.net/attachments/679721816318803975/823299613812719666/PXL_20210321_205742253.jpg" height="150">
</p>

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python distributed_twizzlers_sender.py
 ...
 ```

**\*\*\*Include a picture of your setup here: what did you see on MQTT Explorer?\*\*\***
![1245080](https://user-images.githubusercontent.com/6706384/200462129-152636c4-7bf5-46d1-aaea-06b5139f3600.jpg)
![twizzer](https://user-images.githubusercontent.com/6706384/200461716-617e8664-2cb5-4d3a-9f4f-04a91c26f39d.png)

**\*\*\*Pick another part in your kit and try to implement the data streaming with it.\*\*\***
![proximity](https://user-images.githubusercontent.com/6706384/200461792-ee87f2b6-9f81-4076-a92e-39fa0089a080.png)

[code](proximity_sender.py)


### Part D
### The One True ColorNet

It is with great fortitude and resilience that we shall worship at the altar of the *OneColor*. Through unity of the collective RGB, we too can find unity in our heart, minds and souls. With the help of machines, we can overthrow the bourgeoisie, get on the same wavelength (this was also a color pun) and establish [Fully Automated Luxury Communism](https://en.wikipedia.org/wiki/Fully_Automated_Luxury_Communism).

The first step on the path to *collective* enlightenment, plug the [APDS-9960 Proximity, Light, RGB, and Gesture Sensor](https://www.adafruit.com/product/3595) into the [MiniPiTFT Display](https://www.adafruit.com/product/4393). You are almost there!

<p float="left">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
  <img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
  <img src="https://cdn-shop.adafruit.com/970x728/3595-03.jpg" height="150">
</p>


The second step to achieving our great enlightenment is to run `color.py`. We have talked about this sensor back in Lab 2 and Lab 4, this script is similar to what you have done before! Remember to activate the `circuitpython` virtual environment you have been using during this semester before running the script:

 ```
 (circuitpython) pi@raspberrypi:~ Interactive-Lab-Hub/Lab 6 $ python color.py
 ...
 ```

By running the script, wou will find the two squares on the display. Half is showing an approximation of the output from the color sensor. The other half is up to the collective. Press the top button to share your color with the class. Your color is now our color, our color is now your color. We are one.

(A message from the previous TA, Ilan: I was not super careful with handling the loop so you may need to press more than once if the timing isn't quite right. Also, I haven't load-tested it so things might just immediately break when everyone pushes the button at once.)

You may ask "but what if I missed class?" Am I not admitted into the collective enlightenment of the *OneColor*?

Of course not! You can go to [https://one-true-colornet.glitch.me/](https://one-true-colornet.glitch.me/) and become one with the ColorNet on the inter-webs. Glitch is a great tool for prototyping sites, interfaces and web-apps that's worth taking some time to get familiar with if you have a chance. Its not super pertinent for the class but good to know either way. 

**\*\*\*Can you set up the script that can read the color anyone else publish and display it on your screen?\*\*\***
![S__241213447](https://user-images.githubusercontent.com/6706384/200462170-74e16be0-b911-45d2-bb75-6f20fbcb7bc9.jpg)
![S__241213445](https://user-images.githubusercontent.com/6706384/200462201-d80f4058-8d54-4f48-a38b-4068c0fe950b.jpg)
https://user-images.githubusercontent.com/6706384/200462211-671ca72f-6d7d-4ffa-84a3-3dba976c1b9a.mp4

### Part E


### Make it your own

Find at least one class (more are okay) partner, and design a distributed application together based on the exercise we asked you to do in this lab.

***1. Explain your design*** For example, if you made a remote controlled banana piano, explain why anyone would want such a thing.

In this lab, we developed an MQTT status updator that can interface with multiple existing hospital devices. These devices, send messages across the hospital network, indicating their current status. For example, when the hematology analyzer in the blood department is complete with one task, it can update across the network indicating it is ready. In these examples, we can expidite hospital patient management processes, by providing instantanious situational awareness for multiple departments. Members of our group with hospital backgrounds indicated this manual communication via phone, beepers, etc as a particular painpoint for hospital staff.

***2. Diagram the architecture of the system.*** Be clear to document where input, output and computation occur, and label all parts and connections. For example, where is the banana, who is the banana player, where does the sound get played, and who is listening to the banana music?

![36244192-A099-4CE7-A09D-2BD7B1B5090F](https://user-images.githubusercontent.com/6706384/200461451-7cde8891-7f8a-433d-9a55-30771ef6f86f.jpg)

***3. Build a working prototype of the system.*** Do think about the user interface: if someone encountered these bananas somewhere in the wild, would they know how to interact with them? Should they know what to expect?

See video below for prototype in action. As far as the user interface goes, we are still developing a centralized visual indicator for equipment and status updates. This is quite diffcult to implement as we are unsure of the complex workings of hospital requirements. However, we do understand the need for a dasboard and customization options which can put hospital members in quick communication with one another.

Currently the interface being demonstrated shows the raw interface with the MQTT explorer as a working prototype.

<img width="1123" alt="Screen Shot 2022-11-07 at 9 37 13 PM" src="https://user-images.githubusercontent.com/6706384/200461425-a2e1e302-3183-4208-9b62-213fdda56eb6.png">

In this proposed dashboard we are utilizing Django, and PostgreSQL to manage the MQTT message database and deliver a web format dashboard.

In the above illustration, we show the status using red/green nogo/go indication, with queue represented by the blue squares below.  We also show that this is a personalized chart for the equipment Dr. Wang is most interested in viewing, and that she may logout and switch users if she chooses.

***4. Document the working prototype in use.*** It may be helpful to record a Zoom session where you should the input in one location clearly causing response in another location.

https://youtu.be/c4wwQdWHIvI
