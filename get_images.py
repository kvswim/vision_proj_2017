#Kyle Verdeyen
#Computer Vision 600.431 Final Project
#get_images.py: captures images for use in training known user database
#point rpi at subject and run this, will capture and save to ./subjectimages
#usage: python get_images.py <subjectnumber> 
import sys
import io
import time
import picamera

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

#now to record and split
#we require about 3-5000 images of both positive and negative examples
#in order to train a Haar Cascade
#60fps for 60 seconds theoretically 3600
#90 fps needs 56 seconds to capture 5000!
#set: 60 fps, 69 seconds, captured 3316 frames at 55.23 fps
#set: 90 fps, 56 seconds, captured 3198 frames at 57.04 fps
#set: 120 fps, 56 seconds, captured 2999 frames at 53.49 fps
#maybe we're limited by SD disk speed?
#resulting dataset from 3k images of 2 subjects is 560+ MB, gotta scale down to fit into RAM
print("Starting camera...")
#720p60 is plenty of resolution at a framerate that is fast for capture without being too dark
with picamera.PiCamera(resolution = '720p', framerate = 60) as camera:
    #uncomment these if you are running the Pi on a TV or monitor, allows you to see preview to get subject in frame
    #camera.start_preview()
    #time.sleep(2)

    output = SplitFrames()
    print("Starting subject capture, please wait (approx 1 min)...")
    start = time.time()
    camera.start_recording(output, format = 'mjpeg') #sliceable format
    camera.wait_recording(60) #oh boy
    camera.stop_recording()
    finish = time.time()
    print("Capture complete.")
print('Captured %d frames in %d seconds at %.2f fps' % (output.frame_num, (finish-start), output.frame_num/(finish - start)))