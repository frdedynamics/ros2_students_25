from custom_dxl.CustomDXL import CustomDXL
import time
# creating object for Square class
object_dxls = CustomDXL()
object_dxls.open_port()
object_dxls.send_goal_all_joints(goal=[1000, 2665])
time.sleep(2)
object_dxls.send_goal_single_joint(0,2200)
object_dxls.read_pos()