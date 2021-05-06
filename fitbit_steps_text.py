from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import keyboard


geckopath = r'D:\Coding\geckodriver\geckodriver-v0.29.0-win64'
send_updates = True
delay = 120
updates_after_finish = 2 # will send this many more updates the exit

def setup():
    # get creds for email accoutn and fitbit account
    global driver, email_from, email_to, email_password, fitbit_user, fitbit_password
    with open('email.txt','r') as f:
        email_from, email_password, email_to = [x[:-1] for x in f.read().split('\n')[:3]] # yeah I know this is bad. future me: "x[:-1]" is to trim final space
    print(repr(email_from), repr(email_to), repr(email_password))
    with open('fitbit.txt', 'r') as f:
        fitbit_user, fitbit_password = [x[:-1] for x in f.read().split('\n')[:2]]

    # get mouse position of refresh button on desktop app
    fitbit_desktop_app_setup()

    # get mouse position of command line for circuitplayground, connected to servo, to type in commands
    servo_setup()

    # setup selenium
    driver = webdriver.Firefox(geckopath)

    fitbit_login()
    driver.get('https://fitbit.com/activities')

    # set servo to extremes, then back to 0
    for angle in [0,180,0]:
        set_servo_pos(degrees=angle)
        time.sleep(1)

def fitbit_desktop_app_setup():
    global fitbit_refresh_button_location
    # get location on screen of refresh/sync button on fitbit desktop app. this will allow the program to click this to sync with the fitbit cloud, to then use selenium to get the current step number
    time.sleep(0.5)
    print('move mouse to fitbit refresh button, then push shift')
    while not keyboard.is_pressed('shift'):
        pass
    fitbit_refresh_button_location = pyautogui.position()


def servo_setup():
    global mu_command_line_location
    # get location on screen of command line that interfaces with circuit playground. this will allow the program to control the servo, because I couldnt think of a better way
    time.sleep(0.5)
    print('move mouse to mu editor command line, then push shift')
    while not keyboard.is_pressed('shift'):
        pass

    # initialize servo
    mu_command_line_location = pyautogui.position()
    time.sleep(0.5)
    pyautogui.click(mu_command_line_location)
    time.sleep(0.5)
    pyautogui.typewrite("""\n
import time
import board
import pwmio
from adafruit_motor import servo
pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)
servo = servo.Servo(pwm)
\n""")


def sync_steps_with_fitbit_cloud():
    # syncs steps stored locally in the fitbit desktop app with the fitbit cloud servers, allowing selenium to access the most recent step count
    global fitbit_refresh_button_location
    pyautogui.click(fitbit_refresh_button_location)

def set_servo_pos(degrees):
    # sets servo position by clicking on command line connected to circuit playground, then typing commands to set the servo position
    global mu_command_line_location
    pyautogui.click(mu_command_line_location)
    time.sleep(0.5)
    pyautogui.typewrite('\nservo.angle='+str(degrees)+'\n')

def fitbit_login():
    # logs into fitbit website
    global driver, fitbit_user, fitbit_password
    driver.get("https://fitbit.com/login")
    time.sleep(5)
    driver.find_element_by_id('ember673').send_keys(fitbit_user)
    driver.find_element_by_id('ember674').send_keys(fitbit_password)
    driver.find_element_by_id('ember714').click()
    time.sleep(5)

def text(msg):
    # sends update text/email with most recent step count. to send text, email_to look like 1235551234@att.com (depending on your provider)
    global email_from, email_password, email_to
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login(email_from, email_password)
    resp = conn.sendmail(email_from, email_to, msg)
    return resp

def get_fitbit_steps():
    # gets most recent step count from website using selenium
    driver.refresh()
    steps=driver.find_element_by_class_name('value').text
    steps=int(steps.replace(',',''))
    return steps

def main():
    global send_updates, delay

    try:
        setup()
        while 1:
            sync_steps_with_fitbit_cloud()
            time.sleep(5)
            steps = get_fitbit_steps()
            steps_left = 10000-steps
            print(f'steps:{steps},steps left:{steps_left}')

            if send_updates:
                text(str(steps) + ' steps. ' + str(steps_left) + ' steps left until 10,000')

            if steps_left < 6566:
                print('\a')
                text('approaching 10,000')
                set_servo_pos(180)
                updates_after_finish -= 1
                if updates_after_finish <= 0: exit()
            for s in range(delay-5)[::-1]:
                print(s,'seconds left until next check', ' '*10,end='\r')
                time.sleep(1)

    except Exception as e:
        print('something broke:',e)
        text('something broke: ' + str(e))

"""
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
"""


if __name__=='__main__':
    main()
