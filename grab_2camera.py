from __future__ import print_function

import mil as MIL
import os
import sys
import serial
from multiprocessing import Process, Queue

## Setup Multi thread
def MGrab(id, ScannerID, nImage):
    ## Directory Check
    rootdir = "Scanner/{}".format(ScannerID)
    try:
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)
    except OSError:
        print('Error: Creating directory. ' + rootdir)

    # Allocate defaults.
    MilApplication = MIL.MappAlloc(MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilSystem = MIL.MsysAlloc(MIL.M_DEFAULT, MIL.M_SYSTEM_HOST, MIL.M_DEV0, MIL.M_DEFAULT, None)
    MilDisplay_0 = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDisplay_1 = MIL.MdispAlloc(MilSystem, MIL.M_DEFAULT, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer_0 = MIL.MdigAlloc(MilSystem, MIL.M_DEV0, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)
    MilDigitizer_1 = MIL.MdigAlloc(MilSystem, MIL.M_DEV1, MIL.MIL_TEXT("M_DEFAULT"), MIL.M_DEFAULT, None)

    SizeBand_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_BAND, None)
    SizeX_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_X, None)
    SizeY_0 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_Y, None)

    SizeBand_1 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_BAND, None)
    SizeX_1 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_X, None)
    SizeY_1 = MIL.MdigInquire(MilDigitizer_0, MIL.M_SIZE_Y, None)

    MilImageDisp_0 = MIL.MbufAllocColor(MilSystem,
                                      SizeBand_0,
                                      SizeX_0,
                                      SizeY_0,
                                      8 + MIL.M_UNSIGNED,
                                      MIL.M_IMAGE +
                                      MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB,
                                      None)

    MIL.MbufClear(MilImageDisp_0, MIL.M_COLOR_BLACK)

    MilImageDisp_1 = MIL.MbufAllocColor(MilSystem,
                                        SizeBand_1,
                                        SizeX_1,
                                        SizeY_1,
                                        8 + MIL.M_UNSIGNED,
                                        MIL.M_IMAGE +
                                        MIL.M_PROC + MIL.M_DISP + MIL.M_GRAB,
                                        None)

    MIL.MbufClear(MilImageDisp_1, MIL.M_COLOR_BLACK)
    MIL.MdispSelect(MilDisplay_0, MilImageDisp_0)
    MIL.MdispSelect(MilDisplay_1, MilImageDisp_1)

    # Print a message.
    print("-----------------------------\n")

    for i in range(nImage):
        MIL.MdigGrabContinuous(MilDigitizer_0, MilImageDisp_0)
        MIL.MdigGrabContinuous(MilDigitizer_1, MilImageDisp_1)

        # Halt continuous grab.
        MIL.MdigHalt(MilDigitizer_0)
        MIL.MdigHalt(MilDigitizer_1)
        MIL.MbufExport(MIL.MIL_TEXT("{}/{}_FileName{}.tif".format(rootdir, id, i)), MIL.M_TIFF, MilImageDisp_0)

    MIL.MbufFree(MilImageDisp_0)
    MIL.MbufFree(MilImageDisp_1)
    MIL.MdispFree(MilDisplay_0)
    MIL.MdispFree(MilDisplay_1)
    MIL.MdigFree(MilDigitizer_0)
    MIL.MdigFree(MilDigitizer_1)
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
    ser.port = 'COM{}'.format(port)  # counter for port name starts at 0

    # check to see if port is open or closed
    if (ser.isOpen() == False):
        print('The Port COM{} is Open '.format(port))
        # timeout in seconds
        ser.timeout = 10
        ser.open()
    else:
        print('The Port %d is closed'.format(port))
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
            th1 = Process(target=MGrab, args=(1, scanID, 100))
            th2 = Process(target=MGrab, args=(2, scanID, 100))
            MGrab(scanID, 100)
        if ( command == "turnon") :
            TurnOn(scanID)
        if ( command == "turnoff"):
            TurnOff(scanID)

