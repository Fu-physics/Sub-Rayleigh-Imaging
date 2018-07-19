
from instrumental import instrument, list_instruments
#from instrumental.drivers.cameras import uc480
from instrumental.drivers.cameras import uc480
import numpy as np
import time as Time
import matplotlib.pyplot as plt
import xarray as xr
import os
import time as Time


''' 
    --------------------------------------------->   X (1280)
    |           
    |        ______Width________
    |       |                   |
    |       |                   |
    |      High                 |
    |       |                   |
    |       |___________________| 
    |

    Y

  (1024)

'''


class ThorlabsCamer():
    def __init__(self):

        self.insts = list_instruments()
        print(self.insts)
        

    def ConnectCamera(self):
        self.cam = instrument(self.insts[0])
        print(self.cam)



    def SetCamera(self, yshift = 0, xshift = 0, high = 1024, width = 1280, exposeTime = "0.01[ms]"):
        self.yshift = yshift
        self.xshift = xshift

        self.high = high
        self.width = width

        self.exposure_time = str(exposeTime/1000.0) + "[ms]"

        print("(yshift , xshift , high, width) is: ", yshift, xshift, high, width)
        print("Camera Set !")


    def SingleImageData(self, infoObjSingle):
        try:
            self.cam.start_capture(left = self.xshift, right = self.xshift + self.width, top = self.yshift,
                            bot = self.yshift + self.high, exposure_time = self.exposure_time)
            image = self.cam.get_captured_image(timeout='1s', copy=True)
        except Exception:
            print("ERROR OCCURE !")
            infoObjSingle.appendPlainText("ERROR OCCURE !")

        else:
            return image


    def MultiImageData(self, infoObj,  frame_number_expected = 100, segment_frame = 50):

        t0 = Time.time()

        for j in range(int(frame_number_expected / segment_frame)):
            # Initialized the image data for each segment_fame
            self.data = self.SingleImageData(infoObj)
            print("The {}th segment".format(j))

            for i in range(segment_frame - 1):  # because that initial data is not an empty space.

                data_temp = self.SingleImageData(infoObj)

                # Time.sleep(0.05)
                self.data = np.append(self.data, data_temp, axis=0)

            print("the data shape is:", self.data.shape)
            infoObj.appendPlainText("the data shape is:" + str(self.data.shape))
            np.save('camera_{}_{}'.format(frame_number_expected, j), self.data.astype(np.uint8))
            del self.data
        
        infoObj.appendPlainText("Time consumed to save the data is:" + str(Time.time() - t0) )

        print("Time consumed to save the data is:", Time.time() - t0)



class ReadData():

    def __init__(self, noteObj, frameNumber, segmentFrame, width, high, fileName = "NoGlass"):

        self.frameNumber = frameNumber
        self.segmentFrame = segmentFrame
        self.width = width
        self.high = high
        self.fileName = fileName

        self.image = np.load('camera_{}_0.npy'.format(self.frameNumber))
        print("The segment data shape is: ", self.image.shape)
        self.noteObj = noteObj
        #self.noteObj.appendPlainText("the data has saved as .nc file! ")


    def ImageData(self):

        for j in range(1, int(int(self.frameNumber / self.segmentFrame))):
            temp_data = np.load('camera_{}_{}.npy'.format(self.frameNumber, j))
            # print(temp_data.shape)
            self.image = np.append(self.image, temp_data, axis=0)

        self.image = np.reshape(self.image, [self.frameNumber, self.high, self.width])

        print("The dataForSave shape is: ", self.image.shape)

        #exposure_time = self.expose_spinbox.value()
        exposureTime = 1

        ## note that here we have change the data type uint8 --> int16
        
        ds = xr.Dataset({'CameraMatrix': (['frameNumber', 'high', 'width'], self.image.astype(np.int16))},
                        attrs={'frameNumber': self.frameNumber, 
                            'width':self.width,
                            'hight':self.high,
                            'exposure_time': exposureTime, 
                            "note":self.noteObj.toPlainText()}
                        )


        print(self.noteObj.toPlainText())
                
        return ds 
        
        #ds.to_netcdf(self.fileName + '.nc')


if __name__ == "__main__":
    cam = ThorlabsCamer()
    cam.ConnectCamera()
    cam.SetCamera()
    data = cam.SingleImageData()
    cam.MultiImageData()

    plt.subplot(111)
    plt.imshow(data)
    plt.colorbar()

    #plt.savefig('oneframe.eps', format='eps', dpi=300)

    plt.show()