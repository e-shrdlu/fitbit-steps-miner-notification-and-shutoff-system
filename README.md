# fitbit steps miner notification and shutoff system

Are you a nerd stuck in online PE? Do you have trouble getting your fitbit steps in? Well I have a tool for you: introducing the all new fitbit steps handler (batteries not included)

## what is this?

Essentially, a digital and physical Rube Golberg machine that gets steps on your fitbit

## that.. didnt help much

Okay Ill try again:

I'm taking online PE and I don't feel like gettin 10,000 steps 3 days a week, so I tied my fitbit to my fan, and looped the string through my door handle (causing an up-down motion, getting me steps). Well, one day I forgot to turn it off when I left the house, and I got 12,000 steps. Not too unreasonable, but if I had gotten much more I could have been caught. So, I wrote a script that would text me once I got near 10,000 so I could come turn it off, and then I realized it wouldn't be that hard to connect a servo that would turn off my fan for me. This is that script

## how does it work?

It's pretty convoluted, but here we go: First, it uses pyautogui to click the 'sync' button on the fitbit desktop app, which syncs the step count with the fitbit website. Then, it uses selenium to login to the fitbit website and get the most recent step count (because getting the step count directly from the desktop app would have required some kind of OCR thing since it's not copy-able text). Then it sends a text to the user notifying them of the remaining steps until 10,000. It does this by emailing `<phone number>@<provider>`, which will text your phone. It repeats this every two minutes. If it finds the step count to be above 9900 (heres where it gets bad), it will click a window the user should have already opened up, which serves as command line interface for a circuit playground express, and type in some CircuitPython code that rotates the servo 180 degrees. The servo should be placed next to a weight (in my case a small bag of rocks), which will be knocked off of the desk, which is then connected to a string that pulls the light switch off (because the servo is not strong enough to turn off the lights on its own).

## how do I use it?

I would recommend you don't, but if you insist:

1) download the latest version of geckodriver (for selenium to work)
2) make a new gmail account and enable 'less secure third party app access' under security settings (to send texts/email updates with)
3) make a text file named `email.txt`, the first 3 lines of which should be your new email address, your new email password, and the email to send notifications to (if you want to text instead put `<phone number>@<provider>`, where provider is your providers email according to this link: https://www.mfitzp.com/email2sms
4) make a text file named `fitbit.txt`, with your username and password on the 1st and 2nd lines
5) setup your circuit playground with a servo and install MU editor, according to these guides: https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code, https://github.com/adafruit/Adafruit_CircuitPython_Bundle, https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-servo
6) open the fitbit desktop app and find the 'sync button'
7) open the MU editor and open the command line to the circuit playground
8) run the program and follow the instructions
9) profit

## wouldn't it be easier to do ______?

yes

## shouldn't you be getting exercise though?

yes

## do you really think anyone is going to actually use this?

probably not, I'm not sure why I'm spending so much time writing a readme. That was like 15 whole mintues
I wonder if anyone will even read any this. if you are, you are either bored or stalking me

## aaand thats about it.
dont forget to like and subscribe
