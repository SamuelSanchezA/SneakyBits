
"""
Program summary:

This program takes in a sound file and a picture.
We grab the pixel values (red, green, blue) from the
picture and hide those values inside the channels of
the sound file. The program then creates a new sound file containing
the hidden image. Furthermore, this program is also able
to retrieve the image from the sound file that contains the image.

LINUX VARIANT/ Python 2.7
"""


import soundfile as sf #To read the samples in our sound file
from PIL import Image #To create an image
import Tkinter as tk
import tkFileDialog as filedialog
import tkMessageBox
import os

######################################################################################
def newImage(picLoc, soundLoc):
    """
    Extracting the image from the sound file
    that contains the image hidden inside.
    """ 
    print "Starting extraction process"
    try:
        sound, rate = sf.read(soundLoc)

        width = abs(int(sound[0][0] * offsetW_H)) + 1
        height = abs(int(sound[0][1] * offsetW_H)) + 1
        
        index = 1

        #print ("New image function")#Just printing the first 5 samples of the sound file
        #print (sound[:5])

        #Here we're creating a white picture.
        res = (width,height)
        rgb = (255,255,255)
        pic = Image.new("RGB", res, rgb)

        pixel = pic.load() #Grabbing the pixel values of our white picture.

        #Retrieving the pixel values from our sound file here.
        #And assigning it to our white picture.
        right = 1
        left = 0
        print "Extracting image"
        for x in range(0,res[0]):
            for y in range(0,res[1]):
                if(index % 2 == 0):
                    pixel[x,y] = ((int(sound[index][left]*offset)),
                                  (int(sound[index + 1][right]*offset)),
                                  (int(sound[index + 2][left]*offset)))
                    index = index + 3
                else:
                    pixel[x,y] =((int(sound[index][right]*offset)),
                                (int(sound[index + 1][left]*offset)),
                                (int(sound[index + 2][right]*offset)))
                    index = index + 3


        #pic.show()#Displaying our picture
        pic.save("Extracted_Photos/newImage.bmp") # New Image
        print "Extraction complete"
    except:
        tkMessageBox.showwarning("Error", "No Sound selected")
##########################################################################################
def setMusic(PicLoc, soundLoc):
    """
    This is where we hide the picture inside the sound file.
    """
    if True:
        loadPic = Image.open(str(picLoc),"r")#Loading up the pic we want to hide.
        width = loadPic.size[0] #Getting the width of the pic
        height = loadPic.size[1] #Getting the height of the pic
        data, samplerate = sf.read(soundLoc)
        count = 0
        
        """
        # Error Checking
        print ("Frames and channels",data.shape)
        print ("Samplerate:", samplerate)
        print (len(data))
        print (data[:6])
        """

        rgb = gettingPixelValues(picLoc) #Calling our gettingPixelValues function

        #This runs through each sample in the sound file and assigns the RGB value of the pic to the sample.

        print "Setting values"

        for x in range(1, width * height * 3):
            if(x % 2 == 0):
                data[x][0]= rgb[count]/offset
            else:
                data[x][1]=rgb[count]/offset


            count+=1

        for y in range(width * height * 3, len(data)):
            if(y % 2 == 0):
                data[y][0]= 0
            else:
                data[y][1]= 0
                
        data[0][0] = width / offsetW_H
        data[0][1] = height / offsetW_H
        
        '''
        print (data[:6])
        '''
        #We create our new sound file containing our image.
        filePath = "Embedded_Soundfiles/embeddedSound.wav"
        sf.write(filePath, data, samplerate)
        print "Picture embedded"
    else:
        tkMessageBox.showwarning("Error", "No Image selected")

########################################################################################
def gettingPixelValues(picLoc):
    """
    This function creates and returns a list of all the RGB values of
    the picture you want to hide inside the sound file.
    """
    loadPic = Image.open(picLoc,"r")#Loading up the pic we want to hide.

    pixel = loadPic.load()

    colorList = []

    #getting the rgb values for all the pixel in the image
    for x in range(loadPic.size[0]):
        for y in range(loadPic.size[1]):
            value = pixel[x,y] #Converting tuple into a list
            colorList.append(value[0])
            colorList.append(value[1])
            colorList.append(value[2])

    #print (colorList[:6])
    print "Fetching pixel values"
    return colorList
###################################################################################



#Increasing this number will give rid of the high pitch sound in the background,
#but at the cost of the image quality
#This number seems to fit well with preserving the pic and the sound
offset = 165000.0
offsetW_H = 10000.0
picLoc = ""
soundLoc = ""

if(not os.path.exists("Extracted Photos")):
    os.mkdir("Extracted Photos")
if(not os.path.exists("Embedded Soundfiles")):
    os.mkdir("Embedded Soundfiles")



###################################################################################################
#UI Starts here

# Pop up page for GUI
def chooseFile(a):
    global picLoc
    global soundLoc
    # Files are chosen
    if (a==0):
        tkMessageBox.showinfo("SneakyBits", "Make sure the file is a .png or .jpg format")
        picLoc = filedialog.askopenfilename()
        formatSuffix = picLoc[len(picLoc) - 3:len(picLoc)]
        formatSuffix = formatSuffix.lower()
        while(formatSuffix != "png" and formatSuffix != "jpg"):
            tkMessageBox.showwarning("Error","Has to be .png or .jpg format")
            picLoc = filedialog.askopenfilename()
            if(picLoc == ""):
                break
    elif (a==1):
        tkMessageBox.showinfo("SneakyBits", "Make sure the file is a .wav format")
        soundLoc = filedialog.askopenfilename()
        formatSuffix = picLoc[len(soundLoc) - 3:len(soundLoc)]
        formatSuffix = formatSuffix.lower()
        while(soundLoc[len(soundLoc) - 3:len(soundLoc)] != "wav"):
            tkMessageBox.showwarning("Error","Has to be .wav format")
            soundLoc = filedialog.askopenfilename()
            if(soundLoc == ""):
                break

    print (picLoc)
    return picLoc

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

# Hide picture page
class HidePicture(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       button1 = tk.Button(self, text = "Choose Picture to Hide", command = lambda:chooseFile(0))
       button2 = tk.Button(self, text = "Choose Audio to Hide In", command = lambda:chooseFile(1))
       button3 = tk.Button(self, text = "Go", command = lambda:setMusic(picLoc, soundLoc))
       button1.pack(side="top", fill="both", expand=True)
       button2.pack(side="top", fill="both", expand=True)
       button3.pack(side="top", fill="both", expand=True)
# Extraction page
class ExtractPicture(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       button1 = tk.Button(self, text = "Choose Sound File", command = lambda:chooseFile(1))
       button2 = tk.Button(self, text = "Go", command = lambda:newImage(picLoc, soundLoc))
       button1.pack(side="top", fill="both", expand=True)
       button2.pack(side="top", fill="both", expand=True)

# Framework for pages
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = HidePicture(self)
        p2 = ExtractPicture(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Hide a picture", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Extract a picture", command=p2.lift)

        b1.pack(side="left", fill="x", expand=True)
        b2.pack(side="left", fill="x", expand=True)

        p1.show()



if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Sneaky Bits")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()

#End of UI