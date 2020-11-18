from __future__ import print_function

import mil as MIL
import os
import sys
import serial
from multiprocessing import Process, Queue, Event

## Setup Multi thread
def MGrab(id, ScannerID, nImage, DeviceID):
    ## Directory Check
    rootdir = "Scanner/{}".format(ScannerID)
    try:
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)
    except OSError:
        print('Error: Creating directory. ' + rootdir)

    # Allocate defaults.
    MilApplication = MIL.MappAlloc(MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilSystem = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_HOST,DeviceID, MIL.M_DEFAULT, None)
    MilDisplay = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer = MIL.MdigAlloc(MilSystem,DeviceID, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)

    SizeBand = MIL.MdigInquire(MilDigitizer, MIL.M_SIZE_BAND, None)
    SizeX = MIL.MdigInquire(MilDigitizer, MIL.M_SIZE_X, None)
    SizeY = MIL.MdigInquire(MilDigitizer, MIL.M_SIZE_Y, None)


    MilImageDisp = MIL.MbufAllocColor(MilSystem,
                                      SizeBand,
                                      SizeX,
                                      SizeY,
                                      8 + MIL.M_UNSIGNED,
                                      MIL.M_IMAGE +
                                      MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB,
                                      None)

    MIL.MbufClear(MilImageDisp, MIL.M_COLOR_BLACK)

    MIL.MdispSelect(MilDisplay, MilImageDisp)

    # Print a message.
    print("-----------------------------\n")

    for i in range(nImage):
        MIL.MdigGrabContinuous(MilDigitizer, MilImageDisp)

        # Halt continuous grab.
        MIL.MdigHalt(MilDigitizer)
        MIL.MbufExport(MIL.MIL_TEXT("{}/{}_FileName{}.tif".format(rootdir, id, i)), MIL.M_TIFF, MilImageDisp)

    MIL.MbufFree(MilImageDisp)
    MIL.MdispFree(MilDisplay)
    MIL.MdigFree(MilDigitizer)
    MIL.MsysFree(MilSystem)
    MIL.MappFree(MilApplication)

    return

def ScanIDtoPort(scanID):
    portarray = { "0":[3, 4], "1":[4,5], "2":[6,7]}
    return portarray[scanID]

def TurnOn(scanID):
    print("Scanner {} Turn on ".format(scanID))
    Ports = ScanIDtoPort(scanID)
    for port in Ports:
        sendsignal(port, 'vp')
    return

def TurnOff(scanID):
    print("Scanner {} Turn on ".format(scanID))
    Ports = ScanIDtoPort(scanID)
    for port in Ports:
        sendsignal(port, 'sp')
    return

def sendsignal(port, command):
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = 'COM{}'.format(port-1)  # counter for port name starts at 0

    # check to see if port is open or closed
    if (ser.isOpen() == False):
        print('The Port COM{} is Open '.format(port))
        # timeout in seconds
        ser.timeout = 10
        ser.open()
    else:
        print('The Port %d is closed'.format(COMPORT))
    ser.write(b'{}\r\n'.format(command))
    ser.close()


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if len(sys.argv) >= 3 :
        command = sys.argv[1]
        print("Command: {}".format(command))
        scanID = sys.argv[2]
        if ( command == "scan") :
            trigger_event = Event()
            th1 = Process(target=MGrab, args=(1, scanID, 100, MIL.M_DEV0))
            th2 = Process(target=MGrab, args=(2, scanID, 100, MIL.M_DEV1))
            th1.start()
            th2.start()
            th1.join()
            th2.join()
        if ( command == "turnon") :
            TurnOn(scanID)
        if ( command == "turnoff"):
            TurnOff(scanID)

