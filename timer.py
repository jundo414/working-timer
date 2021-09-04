'''
Working Timer
------
*1  If you are running the program for the first time in a Windows environment, run the following command to enable speechreading.
        $ pip install pywin32
*2  Before running the program, prepare the following configuration file (config.ini).
        [DEFAULT]
        TimeWork = 50    ; time span for working (min)
        TimeBreak = 10   ; time span for breaking (min)
        Iteration = 5    ; number of Iteration
'''

try:
    import tkinter as tk # for python3
    import tkinter.font as font
except:
    import Tkinter as tk # for python2
    import Tkinter.font as font

#import sys
#import logging
import platform
import time
import configparser

#logging.basicConfig(level=logging.DEBUG)

class TimerApp(tk.Frame):

    def __init__(self, time_work, time_break, iteration, master=None):
        tk.Frame.__init__(self, master)
        
        self.started = False
        self.sv_session = tk.StringVar()
        self.sv_status = tk.StringVar()
        self.sv_start_stop = tk.StringVar()
        self.sv_echo = tk.StringVar()

        self.time_work = time_work
        self.time_break = time_break
        self.iteration = iteration

        self.time = time_work

        self.cnt_session = 0
        self.sv_session.set('Session ' + str(self.cnt_session) + ' / ' + str(self.iteration))
        self.sv_status.set(u'')
        self.sv_start_stop.set(u'Start')
        self.sv_echo.set('%02d:00' % (self.time))
        self.sec = 60 * self.time
        self.session_max = self.iteration

        self.flg_working = False
        self.flg_suspend= False

        self.font_default = font.Font(family="Arial",size=24)
        self.font_button = font.Font(family="Arial",size=20)
        self.font_time = font.Font(family="Krungthep",size=60,weight="bold")
        
        self.master.title('Working Timer')
        self.master.geometry('520x230')

        # Start/Stop button
        self.button=tk.Button(self, textvariable=self.sv_start_stop, command=self.start_stop, font=self.font_button, width=20, height=2)
        self.button.grid(row=0, column=0, sticky='news', padx=5, pady=15)

        # Reset button
        self.button=tk.Button(self, text=u'Reset', command=self.reset, font=self.font_button, width=20, height=2)
        self.button.grid(row=0, column=1, sticky='news', padx=5, pady=15)

        # label for session number
        self.label = tk.Label(self, textvariable=self.sv_session, font=self.font_default)
        self.label.grid(row=1, column=0, columnspan=2, sticky='nws', padx=5, pady=5)

        # label for status
        self.label = tk.Label(self, textvariable=self.sv_status, font=self.font_default)
        self.label.grid(row=2, column=0, sticky='nws', padx=5, pady=5)

        # label for remaining time
        display = tk.Label(self, textvariable=self.sv_echo, font=self.font_time, bg='white', fg='black')
        display.grid(row=2, column=1, sticky='nws', padx=5, pady=5)

    def start_stop(self):
        #logging.debug('start_stop()')

        # if you press the "Start" button
        if not self.started:
            if self.flg_suspend is False:
                self.cnt_session += 1
                self.sv_session.set('Session ' + str(self.cnt_session) + ' / ' + str(self.iteration))

            self.sv_status.set(u'Working')
            self.sv_start_stop.set(u'Stop')
            self.after(1000, self.counting)
            self.started = True
            self.flg_working = True
            self.flg_suspend = False
            
            #logging.debug("DEBUG: sterted")
        # if you press the "Stop" button
        else:
            if self.flg_working:
                self.sv_status.set(u'Working (Suspended)')
            else:
                self.sv_status.set(u'Breaking (Suspended)')

            self.sv_start_stop.set(u'Start')
            self.started = False
            self.flg_suspend = True
            #logging.debug("DEBUG: else")

    def counting(self):
        #logging.debug('counting()')
        if self.started:
            self.sv_echo.set('%02d:%02d' % (self.sec/60, self.sec%60))

            #logging.debug('self.flg_working: ' + str(self.flg_working) + ", self.cnt_session: " + str(self.cnt_session) + ", self.iteration: " + str(self.iteration))
            if self.flg_working is True and self.cnt_session <= self.iteration:
                #logging.debug("self.sec(t1): " + str(self.sec))
                if self.sec < 0:
                    #self.sv_echo.set('%02d:%02d' % (self.sec/60, self.sec%60))
                    message = "Please finish the work."
                    # for Windows Env.
                    if platform.system() == "Windows":
                        import win32com.client as wincl
                        voice = wincl.Dispatch("SAPI.SpVoice")
                        voice.Speak(message)
                    # for Mac Env.
                    else:
                        import os
                        os.system('say -v Samantha %s' % message)
                    time.sleep(3)

                    self.time = self.time_break
                    self.sec = 60 * self.time
                    self.sv_echo.set('%02d:00' % (self.time))
                    self.flg_working = False
                    self.sv_status.set(u'Breaking')
                
                self.after(1000, self.counting)
                self.sec -=1

            elif self.flg_working is False and self.cnt_session < self.iteration:
                #logging.debug("self.sec(f1): " + str(self.sec))
                if self.sec < 0:
                    message = "Break time is over. Please start your work."
                    # for Windows Env.
                    if platform.system() == "Windows":
                        import win32com.client as wincl
                        voice = wincl.Dispatch("SAPI.SpVoice")
                        voice.Speak(message)
                    # for Mac Env.
                    else:
                        import os
                        os.system('say -v Samantha %s' % message)
                    time.sleep(3)

                    self.time = self.time_work
                    self.sec = 60 * self.time
                    self.sv_echo.set('%02d:00' % (self.time))
                    self.flg_working = True
                    self.cnt_session += 1
                    self.sv_session.set('Session ' + str(self.cnt_session) + ' / ' + str(self.iteration))
                    self.sv_status.set(u'Working')

                #logging.debug("self.sec(f2): " + str(self.sec))

                self.after(1000, self.counting)
                self.sec -=1
            else:
                message = "All sessions have been completed. Good job today."
                # for Windows Env.
                if platform.system() == "Windows":
                    import win32com.client as wincl
                    voice = wincl.Dispatch("SAPI.SpVoice")
                    voice.Speak(message)
                # for Mac Env.
                else:
                    import os
                    os.system('say -v Samantha %s' % message)
                #logging.debug("セッション終了")
                
                self.cnt_session = 0
                self.sv_session.set('Session ' + str(self.cnt_session) + ' / ' + str(self.iteration))
                self.sv_status.set(u'')
                self.sv_start_stop.set(u'Start')
                self.sv_echo.set('%02d:00' % (self.time))
                self.sec = 60 * self.time
                self.session_max = self.iteration

                self.started = False
                self.flg_suspend = False
            
    def reset(self):
        #logging.debug("DEBUG: reset")
        self.cnt_session = 0
        self.sv_session.set('Session ' + str(self.cnt_session) + ' / ' + str(self.iteration))
        self.sv_status.set(u'')
        self.sv_echo.set('%02d:00' % (self.time))
        self.sec = 60 * self.time
        self.session_max = self.iteration

        if not self.started:    
            self.started = False
            self.flg_suspend = False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    time_work = config.getint("DEFAULT", "TimeWork")
    time_break = config.getint("DEFAULT", "TimeBreak")
    iteration = config.getint("DEFAULT", "Iteration")

    app = TimerApp(time_work, time_break, iteration)
    app.pack()
    app.mainloop()