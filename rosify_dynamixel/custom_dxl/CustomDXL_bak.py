
import dynamixel_sdk as dxl
import numpy as np
from adatools import utils
from sys import exit

## This custom class is created based on dynamixel_sync_read_write.py.

class CustomDXL:
  def __init__(self,dxl_ids=[60, 61],port='/dev/ttyUSB0', baudrate=1000000):
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

    #######################################################
    # Set up the connection to the motors and enable torque
    #######################################################
    # Initialize PortHandler and PacketHandler instance
    self.portHandler = dxl.PortHandler(self.port)
    self.packetHandler = dxl.PacketHandler(self.protocol_version)  # Protocol version  2.0

    # Initialize GroupSyncWrite instance
    self.groupSyncWrite = dxl.GroupSyncWrite(self.portHandler, 
                                              self.packetHandler, 
                                              self.addr_goal_position, 
                                              self.len_goal_position)

    # Initialize GroupSyncRead instace for Present Position
    self.groupSyncRead = dxl.GroupSyncRead(self.portHandler, 
                                            self.packetHandler, 
                                            self.addr_present_position, 
                                            self.len_present_position)
    print("Motors: ", self.dxl_ids, "initialized.")

  def open_port(self):
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
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, 
                                                                        id, 
                                                                        self.addr_torque_enable, 1)
        if dxl_comm_result != dxl.COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit()
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit()
        else:
            print("Dynamixel has been successfully connected")

  def send_goal_all_joints(self, goal=[1071, 2665]):
    """
    Sends a joint commands to all the motors listed in the initialization.

    Parameters:
      goal (list): the goal positions of the motors according to the in the definition of motor IDs array [dxl_ids]

    Returns:
      None

    Example:
      object_dxls.send_goal_all_joints(goal=[1000, 2665])
    """
    # Check if every connected motor gets a goal position.
    if len(self.dxl_ids) != len(goal):
        print("Number of motors does not match the goal pose.")
        self.safe_exit()
    # Add parameter storage for present position value
    for id in self.dxl_ids:
        dxl_addparam_result = self.groupSyncRead.addParam(id)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead addparam failed" % id)
            quit()

    index = 1
    dxl_goal_position_limits = [0, 4095]         # Goal position limits
    # goal_positions_np = np.random.randint(dxl_goal_position_limits[0], dxl_goal_position_limits[1], size=(len(DXL_IDS))) # Generate random goal position for each servo
    goal_positions_np = np.array(goal)
    print("here", goal_positions_np)
    goal_positions = utils.to4bytes(goal_positions_np) # Convert to 4 byte array

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

  def send_goal_single_joint(self, motor_order:int, joint_val:int):
    """
    Sends a single joint command value.

    Parameters:
      motor_order (int): the order of the motor in the definition of motor IDs array [dxl_ids]
      joint_val (int): goal position

    Returns:
      None

    Example:
      object_dxls.send_goal_single_joint(0,2200)
    """
    self.read_pos()
    print(self.current_pose, type(self.current_pose))
    goal = [int(x) for x in self.current_pose]
    goal[motor_order] = int(joint_val)
    goal_positions_np = np.array(goal)
    goal_positions = utils.to4bytes(goal_positions_np) # Convert to 4 byte array

    # Syncread present position
    dxl_comm_result = self.groupSyncRead.txRxPacket()
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

    # Check if groupsyncread data of Dynamixel#1 is available
    for id in self.dxl_ids:
        dxl_getdata_result = self.groupSyncRead.isAvailable(id, self.addr_present_position, 
                                                            self.len_present_position)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % id)
            quit()

    # Get Dynamixel#1 present position value
    i=0
    dxl_present_position = np.array([])
    for id in self.dxl_ids:
        dxl_present_position = np.append(dxl_present_position, 
                                         self.groupSyncRead.getData(id, self.addr_present_position, 
                                                                    self.len_present_position))
        i = i + 1
    print("")

    ## PART 2
    i=0
    for id in self.dxl_ids:
        self.groupSyncWrite.removeParam(id)
        dxl_changeparam_result = self.groupSyncWrite.addParam(id, goal_positions[i])
        if dxl_changeparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % id)
            quit()
        i = i + 1
    # Syncwrite goal position
    dxl_comm_result = self.groupSyncWrite.txPacket()
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

    # Clear syncwrite parameter storage
    self.groupSyncWrite.clearParam()


    if joint_val == 'q':
        # Close port
        self.portHandler.closePort()
        quit()
    else:
        print("here")
        dxl_comm_result = self.groupSyncRead.txRxPacket()
        print("%s, asdasd" % self.packetHandler.getTxRxResult(dxl_comm_result))
        for id in self.dxl_ids:
            dxl_getdata_result = self.groupSyncRead.isAvailable(id, self.addr_present_position, 
                                                                self.len_present_position)
            print(dxl_getdata_result)
    
  def read_pos(self):
    # Syncread present position
    dxl_comm_result = self.groupSyncRead.txRxPacket()
    if dxl_comm_result != dxl.COMM_SUCCESS:
        print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

    # Check if groupsyncread data of Dynamixel#1 is available
    for id in self.dxl_ids:
        dxl_getdata_result = self.groupSyncRead.isAvailable(id, self.addr_present_position, 
                                                            self.len_present_position)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % id)
            quit()

    # Get Dynamixel#1 present position value
    i=0
    dxl_present_position = np.array([])
    for id in self.dxl_ids:
        dxl_present_position = np.append(dxl_present_position, 
                                          self.groupSyncRead.getData(id, self.addr_present_position, 
                                                                    self.len_present_position))
        print("[ID:%03d] PresPos:%03d\t" % (id, dxl_present_position[-1]), end="")
        i = i + 1
    print("")
    self.current_pose = dxl_present_position

  def safe_exit(self):
    self.groupSyncWrite.clearParam()
    self.portHandler.closePort()
