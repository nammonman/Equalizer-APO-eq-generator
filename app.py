import tkinter as tk
from tkinter import filedialog
from sinesweep import play_sine
from readaudio import trim_audio_section
from audiolevels import calculate_average_volume_segments, calculate_average_volume, calculate_eq
import time
import atexit
import os
import pyperclip

wt = 480
ht = 300
volume = 0.3
bass_extension = 35
wait = 1
intensity = float(1.00)

def delete_file_on_exit(file_path):
    # remove temporary audio file used to calculate parameters
    def cleanup():
        if os.path.exists(file_path):
            os.remove(file_path)
        try:
            if root.winfo_exists():
                root.destroy()
        except tk.TclError:
            pass
    atexit.register(cleanup)

file_path = "trimmed_audio.wav"
delete_file_on_exit(file_path)

def button_pressed():
    playSine.config(state=tk.DISABLED)
    time.sleep(wait)  
    play_sine(volume)
    playSine.config(state=tk.NORMAL)  

def validate_input(value):
    if value.isalpha():
        return False
    else:
        return True

def get_parameter():
    parameter = int(bassEntry.get())
    global bass_extension
    if parameter >= 35:       
        bass_extension = parameter

def volume_slider_change(value):
    global volume
    volume = int(value)/100

def intensity_slider_change(value):
    global intensity
    intensity = int(value)/100

def wait_slider_change(value):
    global wait
    wait = int(value)

def upload_audio_file():
    root = tk.Tk()
    root.withdraw()
    fp = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
    trim_audio_section(fp)

def generate_eq_text():
    avg = calculate_average_volume()
    segment_list = calculate_average_volume_segments()
    output_string = calculate_eq(segment_list,avg,bass_extension,intensity)
    pyperclip.copy(output_string)

root = tk.Tk()
root.title("speaker frequency normaliser thing")
root.geometry(str(wt)+"x"+str(ht))

#buttons
openFile = tk.Button(root, text="open wav file", pady= 10, bg= "white", command=upload_audio_file)
openFile.place(x=wt/4, y=ht/4, anchor="center")

createFile = tk.Button(root, text="copy param text to clipboard", pady= 10, bg= "white", command=generate_eq_text)
createFile.place(x=wt/4, y=2*ht/4, anchor="center")

playSine = tk.Button(root, text="play sine test", pady= 10, bg= "blue", fg="white", command=button_pressed)
playSine.place(x=wt/4, y=3*ht/4, anchor="center")

#playSine = tk.Button(root, text="play sine panning", pady= 10, bg= "blue", fg="white", command=lambda: play_panning(volume))
#playSine.place(x=3*wt/4, y=ht/4, anchor="center")

#inputs

# bass extension
label1 = tk.Label(root, text="enter bass extension (Hz)")
label1.place(x=3*wt/4, y=ht/4-40, anchor="center")

button = tk.Button(root, text="enter", command=get_parameter)
button.place(x=3*wt/4+30, y=ht/4-15, anchor="center")

validate_positive_int = root.register(validate_input)
bassEntry = tk.Entry(root, validate="key", validatecommand=(validate_positive_int, '%P'), width=6)
bassEntry.place(x=3*wt/4-30, y=ht/4-15, anchor="center")
bassEntry.insert(0,"35")

# eq intensity
label3 = tk.Label(root, text="eq intensity")
label3.place(x=3*wt/4, y=2*ht/4-55, anchor="center")

slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=intensity_slider_change)
slider.set(100)
slider.place(x=3*wt/4, y=2*ht/4-25, anchor="center")

# volume
label4 = tk.Label(root, text="volume")
label4.place(x=3*wt/4, y=2*ht/4+10, anchor="center")

slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=volume_slider_change)
slider.set(30)
slider.place(x=3*wt/4, y=2*ht/4+40, anchor="center")

# delay
label5 = tk.Label(root, text="delay (sec)")
label5.place(x=3*wt/4, y=3*ht/4, anchor="center")

waittime = tk.Scale(root, from_=1, to=16, orient=tk.HORIZONTAL, command=wait_slider_change)
waittime.set(1)
waittime.place(x=3*wt/4, y=3*ht/4+30, anchor="center")

root.mainloop()
