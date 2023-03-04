import random
import tkinter as tk
from PIL import Image, ImageTk
#import winsound
import time
from playsound import playsound
import sys
from tkinter import ttk


class BalloonAnalogueRiskTask:
    def __init__(self, master):
        self.master = master
        
        # setup game relevant data
        self.print_to_console = True
        self.log_file = open("log.txt", "a+", buffering=1)
        self.score = 0
        self.pumps = 0
        self.nr_balloons = 30
        self.max_pumps = 50 # maximum number of pumps
        self.game_over = False
        self.start_budget = 1500 #initial money
        self.budget = 1500 - 50 #current money
        self.pump_embursment_sum = 0 # temp variable to store the embursment sum
        self.pump_embursment = 1 #how much is added for each pump
        self.punishment = 50 #how much money is substracted for each balloon
        self.budget = self.start_budget - self.punishment #current money
        
        # get height and width of current window
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        # create the frame for the ballon: 
        self.ballon_frame_w = self.width*0.7
        self.ballon_frame_h = self.height*0.7
        self.ballon_frame = tk.Frame(self.master, width=self.ballon_frame_w, height=self.ballon_frame_h)
        self.ballon_frame.configure(bg='white') 
        # create the frame for the button
        self.button_frame_w = self.ballon_frame_w
        self.button_frame_h = self.height*0.3
        self.button_frame = tk.Frame(self.master, width=self.button_frame_w, height=self.button_frame_h) 
        # create the frame for the bar
        self.bar_frame_w = self.width*0.2
        self.bar_frame_h = self.ballon_frame_h
        self.bar_frame = tk.Frame(self.master, width=self.bar_frame_w, height=self.bar_frame_h)
        
        self.title_frame = tk.Frame(self.master, width=self.width, height=self.height*0.2)
        self.title_frame.grid(row=0, column=1)
        
        self.left_buffer_frame = tk.Frame(self.master)
        
        self.bar_frame.grid(row=1, column=0)
        self.ballon_frame.grid(row=1, column=1)
        self.button_frame.grid(row=2, column=1)
        self.left_buffer_frame.grid(row=1, column=2)
        
        #self.title_frame = tk.Frame(self.master, width=self.width, height=self.height*0.2)
        #elf.title_canvas = tk.Canvas(self.title_frame, width=self.width, height=self.height*0.2)
        #self.title_canvas.pack()
        #self.title_frame.grid(row=0, column=0)
        #self.max_money_label = tk.Label(self.title_frame, text="Max Money: 1500", font=("Arial", 12))
        #self.max_money_label.grid(row=0, column=0, pady=10)
        #self.max_money_label.config(text="Max Money: {}".format(self.start_budget))
        #self.title_label = tk.Label(self.title_frame, text="Balloon Game", font=("Arial", 12))
        
        #self.title_label.grid(row=0, column=0)
        
        # setup the title
        self.title_canvas = tk.Canvas(self.title_frame, width=self.ballon_frame_w, height=self.height*0.1)
        self.title_canvas.pack()
        self.score_label = tk.Label(self.title_canvas, text="Score: 0", font=("Arial", 12))
        self.score_label.config(text="Score: {}".format(self.budget))
        self.title_canvas.create_window(100, 100, window=self.score_label)  
        self.max_money_label = tk.Label(self.title_canvas, text="Max Money: 1500", font=("Arial", 12))
        self.max_money_label.config(text="Max Money: {}".format(self.start_budget))
        self.title_canvas.create_window(300, 100, window=self.max_money_label)  
        self.tries_label = tk.Label(self.title_canvas, text="Balloons Left: {}".format(self.nr_balloons), font=("Arial", 12))
        self.tries_label.config(text="Balloons Left: {}".format(self.nr_balloons))
        self.title_canvas.create_window(500, 100, window=self.tries_label)  
        self.pumps_label = tk.Label(self.title_canvas, text="Pumps: 0", font=("Arial", 12))
        self.title_canvas.create_window(700, 100, window=self.pumps_label)  
        
        # setup the buttons 
        self.button_canvas = tk.Canvas(self.button_frame, width=self.button_frame_w, height=self.button_frame_h)
        self.button_canvas.pack()
        self.pump_button = tk.Button(self.button_frame, text="Pump", font="Helvetica 20 bold", command=self.pump)
        self.button_canvas.create_window(self.button_frame_w*0.1, self.button_frame_h*0.08, window=self.pump_button)
        self.checkout_button = tk.Button(self.button_frame, text="Collect CHF", font="Helvetica 20 bold", command=self.checkout)
        self.button_canvas.create_window(self.button_frame_w*0.9, self.button_frame_h*0.08, window=self.checkout_button)
        
        
        """
        self.score_label = tk.Label(self.button_frame, text="Score: 0", font=("Arial", 12))
        self.score_label.grid(row=1, column=0, pady=10)
        self.score_label.config(text="Score: {}".format(self.budget))
        
        self.max_money_label = tk.Label(self.button_frame, text="Max Money: 1500", font=("Arial", 12))
        self.max_money_label.grid(row=0, column=0, pady=10)
        self.max_money_label.config(text="Max Money: {}".format(self.start_budget))
        
        self.tries_label = tk.Label(self.button_frame, text="Balloons Left: {}".format(self.nr_balloons), font=("Arial", 12))
        self.tries_label.grid(row=1, column=1, pady=10)
        self.tries_label.config(text="Balloons Left: {}".format(self.nr_balloons))

        self.pumps_label = tk.Label(self.button_frame, text="Pumps: 0", font=("Arial", 12))
        self.pumps_label.grid(row=2, column=0, pady=10)
        
        self.instructions = tk.Label(self.button_frame, text="Click the pump button to inflate the balloon", font=("Arial", 12))
        self.instructions.grid(row=3, column=0, pady=10)
        self.checkout_button = tk.Button(self.button_frame, text="Collect CHF", font=("Arial", 12), command=self.checkout)
        self.checkout_button.grid(row=4, column=1, pady=10)
        """
        
        
        # setup the balloon
        self.ballon_background = tk.Canvas(self.ballon_frame, width=self.ballon_frame_w, height=self.ballon_frame_h, bg="white")
        img = Image.open("balloon.jpg")
        self.img_baseheight = int(self.ballon_frame_h*0.1)
        hpercent = (self.img_baseheight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize, self.img_baseheight), Image.Resampling.LANCZOS)
        #img.thumbnail((self.img_baseheight,self.img_baseheight), Image.Resampling.LANCZOS)
        #wpercent = (self.img_basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        #img = img.resize((self.img_basewidth,hsize), Image.Resampling.LANCZOS)
        self.balloon_image = ImageTk.PhotoImage(img)
        self.balloon_label = tk.Label(self.ballon_frame, image=self.balloon_image, borderwidth=0)
        self.balloon_label.grid(row=0, column=0, padx=20)
        self.ballon_background.grid(row=0, column=0)
        
        # setup the moving bar
        self.bar = tk.Canvas(self.bar_frame, width=self.bar_frame_w, height=self.bar_frame_h)
        self.bar.pack()
        self.bar.create_rectangle(self.bar_frame_w*0.4, 0.1*self.bar_frame_h, 0.6*self.bar_frame_w, 0.9*self.bar_frame_h, fill="white", outline="black")
        self.moving_bar = self.bar.create_rectangle(self.bar_frame_w*0.4, 0.0*self.bar_frame_h, 0.6*self.bar_frame_w, 0.0*self.bar_frame_h, fill="light blue")
        self.bar.tag_raise(self.moving_bar)
        # to move the bar up (self.bar_frame_w*0.6, 0.1*self.bar_frame_h, 0.4*self.bar_frame_w, self.bar_frame_h) => bar is at the top
        # bar at the bottom: (self.bar_frame_w*0.4, 0.1*self.bar_frame_h, 0.6*self.bar_frame_w, 0.1*self.bar_frame_h) => bar is at bottom
        self.moving_bar_h = 0.9*self.bar_frame_h
        self.bar.coords(self.moving_bar, (self.bar_frame_w*0.4, 0.9*self.bar_frame_h, 0.6*self.bar_frame_w, 0.9*self.bar_frame_h))
        self.pump_dist = (0.9*self.bar_frame_h - 0.1*self.bar_frame_h)/50
        self.bar.create_text(0.5*self.bar_frame_w, 0.05*self.bar_frame_h, text="Potential Losses for this Balloon", fill="black", font=('Helvetica 12 bold'))
        self.bar.create_text(0.5*self.bar_frame_w, 0.08*self.bar_frame_h, text="(-50 to 0)", fill="black", font=('Helvetica 12 bold'))
        self.moving_bar_text = self.bar.create_text(0.3*self.bar_frame_w, 0.9*self.bar_frame_h, text=f"{-self.punishment}", fill="black", font=('Helvetica 12 bold'))
        #self.bar_title = tk.Label(self.bar, text="Potential Losses for this Balloon", font=("Arial", 14))
        #self.bar_title.grid(row=0, column=0)
        
    def log(self, msg):
        if self.print_to_console:
            print(f"[*] {msg}")
        self.log_file.write(msg)
        self.log_file.flush()
    
    def burst_chance(self):
        return 1 / (self.max_pumps - self.pumps + 1)
    
    def pump_ballon(self):
        img = Image.open("balloon.jpg")
        self.img_baseheight = int(self.ballon_frame_h*0.1+(self.ballon_frame_h*0.8/self.max_pumps*self.pumps))
        hpercent = (self.img_baseheight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize, self.img_baseheight), Image.Resampling.LANCZOS)
        self.balloon_image = ImageTk.PhotoImage(img)
        self.balloon_label.config(image=self.balloon_image, borderwidth=0)
        
    def reset_ballon(self):
        img = Image.open("balloon.jpg")
        self.img_baseheight = int(self.ballon_frame_h*0.1)
        hpercent = (self.img_baseheight/float(img.size[1]))
        wsize = int((float(img.size[0])*float(hpercent)))
        img = img.resize((wsize, self.img_baseheight), Image.Resampling.LANCZOS)
        self.balloon_image = ImageTk.PhotoImage(img)
        self.balloon_label.config(image=self.balloon_image, borderwidth=0)
    
    def reset_bar(self, max_punish=False):
        self.bar.coords(self.moving_bar, (self.bar_frame_w*0.4, 0.0*self.bar_frame_h, 0.6*self.bar_frame_w, 0.0*self.bar_frame_h))
        self.bar.coords(self.moving_bar_text, (0.3*self.bar_frame_w, 0.9*self.bar_frame_h))
        if max_punish:
            self.bar.itemconfig(self.moving_bar_text, text=f"{-self.punishment}")
        else:
            self.bar.itemconfig(self.moving_bar_text, text=f"{-self.punishment+self.pumps}")
    
    def pump_bar(self):
        # min height = 0.1*self.bar_frame_h
        # max height = 0.9*self.bar_frame_h
        # 0.8*self.bar_frame_h / self.max_pumps * self.pumps
        self.bar.coords(self.moving_bar, (self.bar_frame_w*0.4, 0.9*self.bar_frame_h-(0.8*self.bar_frame_h / self.max_pumps * self.pumps), 0.6*self.bar_frame_w, 0.9*self.bar_frame_h))
        self.bar.coords(self.moving_bar_text, (0.3*self.bar_frame_w, 0.9*self.bar_frame_h-(0.8*self.bar_frame_h / self.max_pumps * self.pumps)))
        self.bar.itemconfig(self.moving_bar_text, text=f"{-self.punishment+self.pumps}")
    
    def checkout(self):
        playsound('casino.wav', False)
        self.nr_balloons = self.nr_balloons - 1
        self.score_label.config(text="Score: {}".format(self.budget))
        self.tries_label.config(text="Balloons Left: {}".format(self.nr_balloons))
        if self.nr_balloons == 0:
                self.game_over = True
                self.pump_button.config(text="Game Over", state="disabled")
                self.checkout_button.config(text="Game Over", state="disabled")
                self.score_label.config(text="Score: {}".format(self.budget))
        else:
            self.pump_button.config(text="Checked Out", state="disabled")
            self.checkout_button.config(text="Checked Out", state="disabled")
            self.ballon_frame.after(1000, self.reset)
            #self.reset()
    
    def pump(self):
        if self.game_over:
            return
        
        #winsound.PlaySound("inflate.wav", winsound.SND_ASYNC)
        playsound('inflate.wav', False)
        # TODO: implement backup
        self.pumps += 1
        self.pump_embursment_sum += 1
        self.budget = self.budget + self.pump_embursment
        self.pumps_label.config(text="Pumps: {}".format(self.pumps))
        
        prob = random.random()
        b_chance = self.burst_chance()
        burst = prob < b_chance
        self.log(f"ballon pumped, nr pumps: {self.pumps}, probability: {prob}, burst chance: {b_chance}, new budget: {self.budget}")
        if burst:
            self.reset_bar(max_punish=True)
            playsound('explosion.wav', False)
            popped_img = Image.open("poppedballoon.jpg")
            self.img_baseheight = int(self.ballon_frame_h*0.1+(self.ballon_frame_h*0.8/self.max_pumps*self.pumps))
            hpercent = (self.img_baseheight/float(popped_img.size[1]))
            wsize = int((float(popped_img.size[0])*float(hpercent)))
            popped_img = popped_img.resize((wsize, self.img_baseheight), Image.Resampling.LANCZOS)
            self.balloon_image = self.balloon_image = ImageTk.PhotoImage(popped_img)
            self.balloon_label.config(image=self.balloon_image, borderwidth=0)
            self.budget = self.budget - self.pump_embursment_sum
            self.nr_balloons = self.nr_balloons - 1
            self.tries_label.config(text="Balloons Left: {}".format(self.nr_balloons))
            if self.nr_balloons == 0:
                self.game_over = True
                self.pump_button.config(text="Game Over", state="disabled")
                self.checkout_button.config(text="Game Over", state="disabled")
                self.score_label.config(text="Score: {}".format(self.budget))
            else:
                #winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                self.score_label.config(text="Score: {}".format(self.budget))
                self.pump_button.config(text="Popped", state="disabled")
                self.checkout_button.config(text="Popped", state="disabled")
                self.ballon_frame.after(2000, self.reset)
            #self.pump_button.config(text="Game Over", state="disabled")
        else: 
            self.pump_ballon()
            self.pump_bar()
            if self.pumps == self.max_pumps:
                self.checkout()
            else:
                self.score_label.config(text="Score: {}".format(self.budget))
                #self.balloon_image = ImageTk.PhotoImage(Image.open("balloon.jpg").resize((int(100 * self.balloon_size), int(100 * self.balloon_size))))
                #self.balloon_label.config(image=self.balloon_image, borderwidth=0)

    def reset(self):
        self.pumps = 0
        self.pump_embursment_sum = 0
        self.budget = self.budget - self.punishment
        self.score_label.config(text="Score: {}".format(self.budget))
        self.pumps_label.config(text="Pumps: {}".format(self.pumps))
        #self.balloon_image = ImageTk.PhotoImage(Image.open("balloon.jpg").resize((100, 100)))
        #self.balloon_label.config(image=self.balloon_image, borderwidth=0)
        self.pump_button.config(text="Pump", state="active")
        self.checkout_button.config(text="Collect CHF", state="active")
        self.reset_bar()
        self.reset_ballon()

# Scale the label when the window size changes
def on_configure(event):
    # Get the fullscreen width and height
    width = root.winfo_width()
    height = root.winfo_height()

# Bind to the <Configure> event of the root window
    
user = sys.argv[1]
print(user)
root = tk.Tk()
#root.configure(bg='white')
root.bind("<Configure>", on_configure) 
root.title('Ballon Game')
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()      
root.minsize(width=screenWidth, height=screenHeight)
#root.attributes('-fullscreen', True)
app = BalloonAnalogueRiskTask(root)
root.mainloop()
