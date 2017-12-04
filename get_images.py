#Kyle Verdeyen
#Computer Vision 600.431 Final Project
#get_images.py: captures images for use in training known user database
#to be run on a Raspberry Pi with camera device, not for PC use
#point rpi at subject and run this, will capture approximately 1000 images and save to ./subjectimages
#usage: python get_images.py <subjectnumber> 
import os
import sys
import io
import time
import picamera
import shutil

#Takes advantage of the "Magic numbers" in JPEG image files to
#split live feed into many different images
#Since all JPEGs start with FF D8 and end with FF D9, we can use this
#as a delimiter
class SplitFrames(object):
    def __init__(self):
        #init sets 0 frames taken, null output
        self.frame_num = 0
        self.output = None

    def write(self, buffer):
        if buffer.startswith(b'\xff\xd8'): #if buffer starts with bytecode FF D8
            if self.output:
                self.output.close()
            #increment frame counter
            self.frame_num += 1
            #set output stream to name image based on frame number
            #USER MUST SET SUBJECT NUMBER AT COMMAND LINE
            #e.g. python get_images.py 1 --> subject1.imagexx.jpg
            self.output = io.open('subject%s.image%02d.jpg' % (sys.argv[1], self.frame_num), 'wb')
        self.output.write(buffer) #out

#record and split
print("Starting camera...")
#720p60 is plenty of resolution at a framerate that is fast for capture without being too dark
with picamera.PiCamera(resolution = '1080p', framerate = 30) as camera:
    #uncomment this if you are running the Pi on a TV or monitor, allows you to see preview to get subject in frame
    #camera.start_preview()
    
    time.sleep(2) #wait for the pi to settle its white balance
    output = SplitFrames()
    print("Starting subject capture, please wait (approx 20 seconds)...")
    start = time.time()
    camera.start_recording(output, format = 'mjpeg') #sliceable format
    camera.wait_recording(40) #oh boy
    camera.stop_recording()
    finish = time.time()
    print("Capture done.")
print("Captured %d frames in %d seconds at %.2f fps." % (output.frame_num, (finish-start), output.frame_num/(finish - start)))


#now to move all the jpg's into the dest folder since SplitFrames doesn't allow us to set destination directory
print("Placing files in destination directory...")
sourcepath = os.getcwd()
source = os.listdir(sourcepath)
destpath = sourcepath + "/subjectimages"
for files in source:
    if files.endswith(".jpg"):
        shutil.move(os.path.join(sourcepath, files), os.path.join(destpath, files))
print("Finished.")