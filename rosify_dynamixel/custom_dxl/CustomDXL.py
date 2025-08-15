import dynamixel_sdk as dxl
import numpy as np
from adatools import utils
import time

# This example shows how to use the Dynamixel SDK send and receive joint positions.
# The example uses the Dynamixel SDK's GroupSyncWrite and GroupSyncRead functions to send and receive data to and from the servos.

class CustomDXL:
    def __init__(self,dxl_ids=[2],port='/dev/ttyUSB0', baudrate=57600):
        # Define some constants
        self.addr_torque_enable          = 64
        self.addr_goal_position          = 116
        self.len_goal_position           = 4         # data byte length
        self.addr_present_position       = 132
        self.len_present_position        = 4         # data byte length
        self.dxl_moving_status_threshold = 2        # dynamixel moving status threshold
        self.baudrate                    = baudrate
        self.protocol_version            = 2.0
        self.port                        = port  # <-- you may need to change the port where the u2d2 is connected
        self.dxl_ids                     = dxl_ids  # [1, 2, 3, 4, 5]
        self.comm_success                = 0

        self.current_pose = [0]*len(self.dxl_ids)

        # Initialize PortHandler and PacketHandler instance
        self.portHandler = dxl.PortHandler(self.port)
        self.packetHandler = dxl.PacketHandler(self.protocol_version)  # Protocol version  2.0
        
        # Initialize GroupSyncWrite instance
        self.groupSyncWrite = dxl.GroupSyncWrite(self.portHandler, self.packetHandler, self.addr_goal_position, self.len_goal_position)

        # Initialize GroupSyncRead instace for Present Position
        self.groupSyncRead = dxl.GroupSyncRead(self.portHandler, self.packetHandler, self.addr_goal_position, self.len_goal_position)


    def open_port(self):
        #######################################################
        # Set up the connection to the motors and enable torque
        #######################################################
        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:  
            print("Failed to open the port")
            quit()

        # Set port baudrate
        if self.portHandler.setBaudRate(self.baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

        # Enable Dynamixel Torque
        for id in self.dxl_ids:
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, self.addr_torque_enable, 1)
            if dxl_comm_result != dxl.COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                quit()
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                quit()
            else:
                print("Dynamixel has been successfully connected")
    def send_goal(self, goal_pos):
        ########################
        # Sending goal positions
        ########################
        # Add parameter storage for present position value
        for id in self.dxl_ids:
            dxl_addparam_result = self.groupSyncRead.addParam(id)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncRead addparam failed" % id)
                quit()

        goal_positions = utils.to4bytes(goal_pos) # Convert to 4 byte array

        # Add goal position values to the Syncwrite parameter storage
        i=0
        for id in self.dxl_ids:
            dxl_addparam_result = self.groupSyncWrite.addParam(id, goal_positions[i])
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % id)
                quit()
            i = i + 1

        # Syncwrite goal position
        dxl_comm_result = self.groupSyncWrite.txPacket()
        if dxl_comm_result != dxl.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        # Clear syncwrite parameter storage
        self.groupSyncWrite.clearParam()


    def send_single_goal(self, motor_order, goal_pos):
        ########################
        # Sending goal positions
        ########################
        # Add parameter storage for present position value
        id = self.dxl_ids[motor_order]
        self.groupSyncRead.clearParam()
        dxl_addparam_result = self.groupSyncRead.addParam(id)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead addparam failed" % id)
            quit()

        goal_position = utils.to4bytes(goal_pos) # Convert to 4 byte array

        # Add goal position values to the Syncwrite parameter storage
        dxl_addparam_result = self.groupSyncWrite.addParam(id, goal_position[0])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % id)
            quit()

        # Syncwrite goal position
        dxl_comm_result = self.groupSyncWrite.txPacket()
        if dxl_comm_result != dxl.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        
        print("reached to ", goal_pos)

        # Clear syncwrite parameter storage
        self.groupSyncWrite.clearParam()



    def read_pos(self, goal_pos):
        #########################
        # Reading servo positions
        #########################
        while 1:
            # Syncread present position
            dxl_comm_result = self.groupSyncRead.txRxPacket()
            if dxl_comm_result != dxl.COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

            # Check if groupsyncread data of Dynamixel#1 is available
            for id in self.dxl_ids:
                dxl_getdata_result = self.groupSyncRead.isAvailable(id, self.addr_present_position, self.len_present_position)
                if dxl_getdata_result != True:
                    print("[ID:%03d] groupSyncRead getdata failed" % id)
                    quit()

            
            # Get Dynamixel#1 present position value
            i=0
            dxl_present_position = np.array([])
            for id in self.dxl_ids:
                dxl_present_position = np.append(dxl_present_position, self.groupSyncRead.getData(id, self.addr_present_position, self.len_present_position))
                print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t" % (id, goal_pos[i], dxl_present_position[-1]), end="")
                i = i + 1
            print("")

            if ((abs(goal_pos - dxl_present_position) < self.dxl_moving_status_threshold).all()):
                break


if __name__ == "__main__":
    object_dxl = CustomDXL()
    object_dxl.open_port()
    object_dxl.send_goal(goal_pos=[2100])
    time.sleep(1)
    # object_dxl.clear_param()
    time.sleep(1)
    object_dxl.send_single_goal(motor_order=0, goal_pos=[100])
    time.sleep(1)
    object_dxl.send_single_goal(motor_order=0, goal_pos=[300])
    time.sleep(1)
    object_dxl.send_single_goal(motor_order=0, goal_pos=[800])
    time.sleep(1)
    object_dxl.send_single_goal(motor_order=0, goal_pos=[1100])
    time.sleep(1)
    object_dxl.send_single_goal(motor_order=0, goal_pos=[1700])
