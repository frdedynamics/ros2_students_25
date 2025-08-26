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
    
    def getIDs(self):
      return self.dxl_ids

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


        # Add parameter storage for present position value
        for id in self.dxl_ids:
            self.groupSyncRead.clearParam()
            dxl_addparam_result = self.groupSyncRead.addParam(id)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncRead addparam failed" % id)
                quit()

    def send_goal(self, goal_pos):

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

    # def read_motor_positions(self):
    #     """
    #     Reads the current present position of all configured Dynamixel motors.
    #     Returns:
    #         list: A list of integer present positions for each motor,
    #               or None if there was a communication error.
    #     """
    #     present_positions = []

    #     # Clear previous parameters before adding new ones for reading
    #     self.groupSyncRead.clearParam()

    #     # Add parameter storage for present position value for each motor
    #     for id in self.dxl_ids:
    #         dxl_addparam_result = self.groupSyncRead.addParam(id)
    #         if dxl_addparam_result != True:
    #             print("[ID:%03d] groupSyncRead addparam failed" % id)
    #             return None # Indicate failure to add all parameters

    #     # Syncread present position
    #     dxl_comm_result = self.groupSyncRead.txRxPacket()
    #     if dxl_comm_result != dxl.COMM_SUCCESS:
    #         print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
    #         return None
        
    #     # Get data from GroupSyncRead parameter storage
    #     for id in self.dxl_ids:
    #         # After a successful txRxPacket, data should be available.
    #         # No need for a separate 'is' check here.
    #         present_position = self.groupSyncRead.getData(id, self.addr_present_position, self.len_present_position)
    #         present_positions.append(present_position)
        
    #     # Clear syncread parameter storage after reading
    #     self.groupSyncRead.clearParam()
        
    #     return present_positions

    def read_motor_positions(self):
        """
        TODO: Doesn't return correct values
        """
        present_positions = []

        # Clear previous parameters before adding new ones for reading
        self.groupSyncRead.clearParam()
        print("Cleared groupSyncRead parameters.")

        # Add parameter storage for present position value for each motor
        for id in self.dxl_ids:
            dxl_addparam_result = self.groupSyncRead.addParam(id)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncRead addparam failed" % id)
                return None # Indicate failure to add all parameters
            print(f"Added ID:{id} to groupSyncRead parameters.")


        # Syncread present position
        print("Attempting to read positions from motors...")
        dxl_comm_result = self.groupSyncRead.txRxPacket()
        if dxl_comm_result != dxl.COMM_SUCCESS:
            print("Error: %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            # Also check for packet errors even if comm result is success for more detailed info
            dxl_error = self.packetHandler.getLastRxPacketError(self.portHandler.getPortNum())
            if dxl_error != 0:
                 print("Packet Error: %s" % self.packetHandler.getRxPacketError(dxl_error))
            return None
        else:
            print("GroupSyncRead txRxPacket successful.")
        
        # Get data from GroupSyncRead parameter storage
        for id in self.dxl_ids:
            # Check if groupSyncRead data is available for the current motor ID
            if self.groupSyncRead.isAvailable(id, self.addr_present_position, self.len_present_position):
                present_position = self.groupSyncRead.getData(id, self.addr_present_position, self.len_present_position)
                present_positions.append(present_position)
                print(f"ID:{id} - Present Position: {present_position}")
            else:
                print(f"[ID:{id}] groupSyncRead data not available for present position.")
                # If data isn't available for one motor, we can either return None
                # or append a placeholder (e.g., -1) and continue.
                # For now, returning None if any read fails.
                return None
        
        # Clear syncread parameter storage after reading
        self.groupSyncRead.clearParam()
        print("Cleared groupSyncRead parameters after reading.")
        
        return present_positions


    


if __name__ == "__main__":
    object_dxl = CustomDXL(dxl_ids=[0,4])
    object_dxl.open_port()
    time.sleep(1)
    object_dxl.send_goal([500, 500])
    time.sleep(1)
    object_dxl.send_goal([2500, 2500])
    
    
