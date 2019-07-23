
import os
import pwd
import sys
import time
import ffmpeg
import pynput
import subprocess
import speech_recognition as sr


# from imports
from copy import copy
from PIL import Image
from io import BytesIO
from selenium import webdriver
from pynput.keyboard import Key, Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class Whats:

    def __init__(self, browser, owner_name, headless=False, verbose=False):

        # Setting keyboard
        self.keyboard = Controller()
        # Creating a variable to the last message and the last audio
        self.last_message = ""
        self.last_audio = ""
        # Setting headless variable
        self.headless = headless
        # Setting verbose variable
        self.verbose = verbose
        # Setting owner_name variable
        self.owner_name = owner_name

        self.create_default_folders()
        
        # Choosing the browser
        if browser == "chrome":
            self.setting_up_chrome()
        elif browser == "firefox":
            self.setting_up_firefox()
        else:
            self.print_parser("We don't know this browser.", error=True, finalize=True)
        
        # Entering on the Whatsapp Web site
        self.print_parser("Loading whatsapp web...")
        self.driver.get("https://web.whatsapp.com")

        # waiting the QR CODE scan
        self.scan_qrcode()
        
        # Waiting the message loading
        time.sleep(10)

        self.change_chat(self.owner_name)
    
    def send_message(self, message, chat):

        self.print_parser("Sending the message: {}\n to chat: {}".format(message, chat))

        self.change_chat(chat)

        # Searching the text box
        textBox = self.driver.find_element_by_xpath("//div[@spellcheck='true']")
        # Checking if the message isn't empty
        if message != "":
            # Adding the bot name to the message
            message = "[Whats Delivery]:\n" + str(message) + "\n"
            # Sending the characteres
            textBox.send_keys(message)
        
        self.change_chat(self.owner_name)
    
    def check_new_message(self):

        self.verbose_parser("Checking for new messages...")

        chat = self.get_first_chat()

        self.change_chat(chat)

        # Catching all the audios
        audios = self.driver.find_elements_by_class_name('_2jfIu')

        # Verifying if there is no audios
        if len(audios) != 0:

            # if audios is not empty, audios_links cannot be empty
            audios_links = self.driver.find_elements_by_tag_name('audio')

            # Waiting audio link appear
            initial_moment = time.time()
            while True:
                actual_moment = time.time()
                if actual_moment - initial_moment > 10:
                    have_audio = False
                    break
                if len(audios_links) == 0:
                    time.sleep(1)
                    audios_links = self.driver.find_elements_by_tag_name('audio')
                else:
                    have_audio = True
                    break
            
            if have_audio:

                new_audio = audios_links[-1].get_attribute('src')

                try:
                    # Mouse hover on the last audio
                    ActionChains(self.driver).move_to_element(audios[-1]).perform()
                    in_screen = True
                except:
                    in_screen = False

                if new_audio != self.last_audio and in_screen:

                    self.last_audio = new_audio

                    # Finding the options button
                    optionsButton = self.driver.find_elements_by_xpath('//div[@data-js-context-icon="true"]')

                    while True:
                        try:
                            # Clicking this
                            optionsButton[-1].click()
                            # Finding the download button
                            downloadButton = self.driver.find_element_by_xpath("//div[@title='Baixar']")
                            break
                        except:
                            # Wait
                            time.sleep(1)

                    # Clicking this
                    downloadButton.click()
                    # Waiting the download
                    time.sleep(3)
                    # Converting ogg to wav
                    os.popen("ffmpeg -i audios/* audios/audio.wav -loglevel panic")
                    # Waiting the conversion
                    time.sleep(1)
                    # GO
                    
                    r = sr.Recognizer()
                    with sr.AudioFile(os.getcwd()+"/audios/audio.wav") as source:
                        audio = r.record(source)

                    try:
                        # This is the result
                        speech = r.recognize_google(audio)
                        speech = '/ ' + speech
                        # Removing the audio
                        files = os.listdir('audios')
                        for file in files:
                            os.remove('audios/'+file)
                        self.change_chat(self.owner_name)
                        return (chat, speech)
                    except Exception as e:
                        self.print_parser("Exception: "+str(e), finalize=True, error=True)

        

        # Catching all the messages
        messages = self.driver.find_elements_by_class_name('_3zb-j')
        if len(messages) != 0:
            # Supposed new message is the last message
            newMessage = messages[-1].text

            # Checking if the new message isn't iqual to the last message
            if newMessage != self.last_message:
                # We have a new message
                self.last_message = newMessage
                self.change_chat(self.owner_name)
                return (chat, newMessage)

            else:
                # No new message
                self.change_chat(self.owner_name)
                return ("","")
        
        self.change_chat(self.owner_name)
        return ("","")

    def get_first_chat(self):

        # div_//div[@class="2FBdJ"]
        # nome .//span[@dir="auto" and @class="_1wjpf"]
        # horario .//span[@class="_3T2VG"]
        chats_div = self.driver.find_elements_by_xpath('//div[@class="_2FBdJ"]')

        chats = {}

        for chat_div in chats_div:
            chat_name = chat_div.find_element_by_xpath('.//span[@dir="auto" and @class="_1wjpf"]').text
            hour_string = chat_div.find_element_by_xpath('.//span[@class="_3T2VG"]').text
            hour = int(hour_string[:2]+hour_string[3:])

            chats[chat_name] = hour
        
        max_hour = max(chats.values())

        for chat_name, hour in chats.items():
            if hour == max_hour:
                return chat_name

    def change_chat(self, chat):

        initial_moment = time.time()
        while True:
            actual_moment = time.time()
            if actual_moment - initial_moment > 10:
                self.print_parser("We can't find {}'s chat.".format(chat), finalize=True, error=True)
            try:
                user = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(chat))
                user.click()
                self.verbose_parser("{}'s chat finded!".format(chat))
                break
            except:
                pass

    def create_default_folders(self):
        # Creating audios and videos folders
        self.verbose_parser("Creating default folders.")
        try:
            # Trying to list files of the audios directory
            files = os.listdir("audios")
            # Passing through all the files
            for file in files:
                # Removing file
                os.remove("audios/{}".format(file))
        except:
            # Creating folder
            os.makedirs("audios")
        
        try:
            # Trying to list files of the videos directory
            files = os.listdir("videos")
        except:
            # Creating folder
            os.makedirs("videos")
    
    def setting_up_chrome(self):
        
        chrome_options = ChromeOptions()
        if self.headless:
            self.verbose_parser("Initializing in headless mode.")
            chrome_options.add_argument("--headless")
        self.verbose_parser("setting up chrome configuration.")

        try:

            self.driver = webdriver.Chrome(chrome_options=chrome_options)

        except:
            
            if os.name=='posix':

                if not os.path.isfile('/usr/local/bin/chromedriver'):

                    os.system('wget https://chromedriver.storage.googleapis.com/2.46/chromedriver_linux64.zip -O /usr/local/bin/cdriver.zip')
                    os.system('unzip /usr/local/bin/cdriver.zip -d /usr/local/bin')
                    self.driver = webdriver.Chrome()

                else:

                    raise EnvironmentError("Selenium error. Tip: do not run this script as root.")

            elif os.name == 'nt':
                
                print('You need to install a corresponding version of the Chrome driver at http://chromedriver.chromium.org/downloads')
                raise EnvironmentError("Chrome driver not installed.")

    def setting_up_firefox(self):

        self.verbose_parser("setting up firefox configuration.")
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("browser.download.dir", "{}/audios".format(os.getcwd()))
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/ogg")
        
        firefox_options = FirefoxOptions()
        if self.headless:
            self.verbose_parser("Initializing in headless mode.")
            firefox_options.headless = True
     
        try:
       
            self.driver = webdriver.Firefox(firefox_profile=firefox_profile, options=firefox_options)
        
        except:
            
            if os.name =='posix':
                if not os.path.isfile('/usr/local/bin/geckodriver'):
                    os.system('sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz -O /usr/local/bin/gecko.tar.gz')
                    os.system('sudo tar xf /usr/local/bin/gecko.tar.gz -C /usr/local/bin/')
                    self.driver = webdriver.Firefox(firefox_profile=profile)
                else:
                    raise EnvironmentError("Selenium error. Tip: don't run this script as root.")
            elif os.name == 'nt':
                print("You need to install the lastest version of gecko driver at: https://github.com/mozilla/geckodriver/releases")
                raise EnvironmentError("Gecko driver not installed")
                    
    def scan_qrcode(self):

        # waiting..
        while True:
            try:
                qrcode = self.driver.find_elements_by_xpath('//img[@alt="Scan me!"]')[0]
                break
            except:
                pass

        src = b""
        self.print_parser("Updating QRCode in your root folder (qrcode.png).")
        while True:

            # checking if qr code was scanned
            try:
                self.verbose_parser("Verifying if qrcode was scanned...")
                qrcode = self.driver.find_elements_by_xpath('//img[@alt="Scan me!"]')[0]
                # if this return a error, qr code was scanned
            except:
                self.verbose_parser("QRCode scanned!")
                break

            try:
                qrcode = self.driver.find_elements_by_xpath('//img[@alt="Scan me!"]')[0]
                
                new_src = qrcode.get_attribute("src")
                new_src = bytes(new_src[22:]+"=", 'utf-8')
                if new_src != src:
                    src = copy(new_src)
                    png = self.driver.get_screenshot_as_png()
                    im = Image.open(BytesIO(png))
                    location = qrcode.location
                    size = qrcode.size
                    left = location['x'] - 10
                    top = location['y'] - 10
                    right = location['x'] + size['width'] + 10
                    bottom = location['y'] + size['height'] + 10
                    im = im.crop((left, top, right, bottom))
                    im.save('qrcode.png')
                    self.verbose_parser("new QR Code downloaded! (qrcode.png)")
                
                time.sleep(1)
                
            except:
                self.print_parser("You didn't scan. Try again.", finalize=True)

    def print_parser(self, message, error=False, finalize=False):

        if error:
            print("[whats] ERROR: {}".format(message))
        else:
            print("[whats] {}".format(message))
        if finalize:
            self.driver.close()
            exit("Exiting...")
    
    def verbose_parser(self, message):

        if self.verbose: self.print_parser(message)
    
    def close(self):
        self.driver.close()
        exit("Exiting...")