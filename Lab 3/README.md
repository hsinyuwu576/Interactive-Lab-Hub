# Chatterboxes
**NAMES OF COLLABORATORS HERE**
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

[**greet_me.sh**](https://github.com/hsinyuwu576/Interactive-Lab-Hub/blob/Fall2022/Lab%203/greet_me.sh)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. 
Now, we need to find out where your webcam's audio device is connected to the Pi. Use `arecord -l` to get the card and device number:
```
pi@ixe00:~/speech2text $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Device [Usb Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
The example above shows a scenario where the audio device is at card 1, device 0. Now, use `nano vosk_demo_mic.sh` and change the `hw` parameter. In the case as shown above, change it to `hw:1,0`, which stands for card 1, device 0.  

Now, look at which camera you have. Do you have the cylinder camera (likely the case if you received it when we first handed out kits), change the `-r 16000` parameter to `-r 44100`. If you have the IMISES camera, check if your rate parameter says `-r 16000`. Save the file using Write Out and press enter.

Then try `./vosk_demo_mic.sh`

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

[**ask_zip_code.sh**](https://github.com/hsinyuwu576/Interactive-Lab-Hub/blob/Fall2022/Lab%203/ask_zip_code%2Csh)

[**ask_zip_code.py**](https://github.com/hsinyuwu576/Interactive-Lab-Hub/blob/Fall2022/Lab%203/ask_zip_code%2Cpy)

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

[**storyboard 1**](https://drive.google.com/file/d/1Diu9WsYSal70g7XKEnVcV2ezFsku4fUp/view?usp=sharing)

[**storyboard 2**](https://drive.google.com/file/d/1Dbvu4dIiNcfAMqlrybzwyR4fhkIseU4S/view?usp=sharing)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

[**document**](https://drive.google.com/file/d/1DtC_qFzJ9Iu1TN7JEtzBUqD5f1HtC1c8/view?usp=sharing)

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

[**Video**](https://drive.google.com/file/d/1v04cyh7-__usiC7C-TfOs-PX0kfq3X7T/view?usp=sharing)

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

Both dialogues were similar. However, the act-out dialogue seems to be more interesting and flexible than what I planned.

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

**Heather's feedback:**
**Henry’s storyboard is really clear and can link back to last lab’s interaction of the clock. This is really like Alexa and it seems like more helpful as it works like a task management tool. The act-out dialogue seems better and I’m looking forward to see more improvements in part2! Keep up with the good work.**


1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...

**I think that the device needs to be able to understand what users say. The users would communicate to device with different tone and wide vocabularies. Therefore, the device needs to understand all of this and the semantic meaning, so we may train NLP model and inference it on the device. Honestly, it is hard to implement and beyond the scope. Hence, in the prototyping step, I will simplify the whole process and just provide the particular input to the device.**

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

**Besides speech, we can use gesture to interact with users. For example, if users want to sleep more time, uses can wave hand to the device.**

3. Make a new storyboard, diagram and/or script based on these reflections.

[**Storyboard 1**](https://drive.google.com/file/d/1EKf88tOkcvRRifnHjqnMMozYZOx7ZIQ9/view?usp=sharing)

[**Storyboard 2**](https://drive.google.com/file/d/1EQE98f7cP6oQLnIafxsegV-u2fKJlPj0/view?usp=sharing)

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

[**Control flow**](https://drive.google.com/file/d/1EER3uUGVtVPlCaQ3CNlnv_IQFX5CjFUk/view?usp=sharing)

*Include videos or screencaptures of both the system and the controller.*

[**System & controller**](https://drive.google.com/file/d/1EGZUXHMlS4e9UHcHBRPX4JXHRa-LmiIY/view?usp=sharing)

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

The system follows the control flow correctly. And it can perform all tasks (set clock, set reminder, wake up users, remind users) smoothly. However, the system is restricted both on input and output side. For the input side, the system is limited by the accuracy of speech to text technology. For the output side, the system just can response with limited vocabulary and robotic tone.

### What worked well about the controller and what didn't?

The controller can recognize hand waving precisely and can wake user up on time. However, the controller has trouble to recognize what user saying. Especially for the reminder part, the controller cannot recognize what users are saying precisely.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

For the system with speech interactions, there is a high technical requirement to design a system that is capable to fully understand users’ meaning and respond with appropriate sentence.


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

The interaction can be created through speech, gesture, body position and screen etc. Moreover, for wearable device, we can capture the users’ biology data and use vibration to interaction with users.
