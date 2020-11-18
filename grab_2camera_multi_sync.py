from __future__ import print_function

import mil as MIL
import os
import sys
import serial
from multiprocessing import Process, Event, Lock
import time

## Setup Multi thread
def MGrab(id, ScannerID, nImage, DeviceID, event, lock):
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

#    MIL.MdispSelect(MilDisplay, MilImageDisp)

    # Print a message.
    print("-----------------------------\n")

    for i in range(nImage):
        MIL.MdigGrabContinuous(MilDigitizer, MilImageDisp)

        # Halt continuous grab.
        MIL.MdigHalt(MilDigitizer)
        MIL.MbufExport(MIL.MIL_TEXT("{}/{}_FileName{}.tif".format(rootdir, id, i)), MIL.M_TIFF, MilImageDisp)
        event.set()
        time.sleep(0)
        lock.acquire()
        lock.release()
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


def scan_sync_event(scanID, count):
    trigger_event1 = Event()
    trigger_event2 = Event()
    locking= Lock()
    locking.acquire()
    th1 = Process(target=MGrab, args=(1, scanID, count, MIL.M_DEV0, trigger_event1, locking))
    th2 = Process(target=MGrab, args=(2, scanID, count, MIL.M_DEV1, trigger_event2, locking))
    th1.start()
    th2.start()
    for i in range(1, count):
        trigger_event1.wait()
        trigger_event2.wait()
        locking.release()
#      print("Event Released ScanID{}_{}".format(scanID, i))
        time.sleep(0)
        locking.acquire()
    locking.release()
    th1.join()
    th2.join()
    print("Test wait")


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    if len(sys.argv) >= 3 :
        command = sys.argv[1]
        print("Command: {}".format(command))
        scanID = sys.argv[2]

        if ( command == "scan") :
            scan_sync_event(scanID, 100)

        if ( command == "turnon") :
            TurnOn(scanID)
        if ( command == "turnoff"):
            TurnOff(scanID)

