from custom_dxl.CustomDXL_2025 import CustomDXL
import time
object_dxl = CustomDXL(dxl_ids=[0,4])
object_dxl.open_port()
time.sleep(1)
object_dxl.send_goal([500, 500])
time.sleep(1)
object_dxl.send_goal([2500, 2500])
