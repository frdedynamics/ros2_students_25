import rclpy
from rclpy.node import Node
import math

from geometry_msgs.msg import Point
from nav_msgs.msg import OccupancyGrid
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from visualization_msgs.msg import Marker

class MapFilterClass(Node):
    def __init__(self):
        super().__init__('MapFilterNode')

        self.map_msg = OccupancyGrid()
        self.mask_size = 6*6

        qos_profile = QoSProfile(reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE,
                        history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
                        durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL,
                        depth=5,
        )

        self.create_subscription(OccupancyGrid, '/map', callback=self.clbk_map, qos_profile=qos_profile)
        
        self.pub_filtered_map = self.create_publisher(OccupancyGrid, 'filtered_map', 10)

        self.pub_marker = self.create_publisher(Marker, 'marker_visual', 2)


        self.marker_msg = Marker()
        #Defines the transformation frame with which the following data is associated
        self.marker_msg.header.frame_id = "/map"
        #Defines the current time in ros time
        self.marker_msg.header.stamp = self.get_clock().now().to_msg()
        #Assign a unique marker id
        self.marker_msg.id = 0
        #Define the type of oject that is displayed
        self.marker_msg.type = Marker.POINTS
        #Define the action that is taken
        self.marker_msg.action = Marker.ADD
        #Define part of the orientation of the object displayed in rviz
        self.marker_msg.pose.orientation.w =1.0
        # Defines the size of the marker (in meters) displayed in rviz
        self.marker_msg.scale.x=0.1
        self.marker_msg.scale.y=0.1
        # Define the color (red, green and blue from 0-1) and the opacity (alpha from 0-1)
        self.marker_msg.color.r = 0.0/255.0
        self.marker_msg.color.g = 255.0/255.0
        self.marker_msg.color.b = 0.0/255.0
        self.marker_msg.color.a = 1.0
        #Define how long the object should last before being automatically deleted, where 0 indicates forever
        self.marker_msg.lifetime = rclpy.duration.Duration().to_msg()

        self.lidar_value = 100.0

        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def clbk_map(self, msg):
        self.og_map_msg = msg

        self.get_logger().info('Map Size: '+str(len(msg.data)))
        self.get_logger().info('Origin Position: '+str(msg.info.origin.position))

        self.map_msg.header = msg.header
        self.map_msg.info.origin = msg.info.origin
        self.map_msg.info.map_load_time = msg.info.map_load_time

        self.reduce_map()

    def get_map_pos(self, map_iter):
        """
        Returns x and y integer values of the map grid given the iteration value of the map list.
        """
        x = int(map_iter/self.map_msg.info.width)
        y = int(map_iter - x*self.map_msg.info.width)

        return [x, y]
    
    def get_world_pos(self, x, y):
        """
        Given the x and y map grid values returns the actual position coordinates in the gazebo world.
        """
        map_position = Point()
        map_position.x = self.map_msg.info.origin.position.x + y*self.map_msg.info.resolution
        map_position.y = self.map_msg.info.origin.position.y + x*self.map_msg.info.resolution

        return map_position
    
    def get_map_iter(self, x, y):
        """
        Given the x and y grid values of the map returns the corresponding map list iteration.
        """
        map_iter = x*self.og_map_msg.info.width + y

        return map_iter
    
    def avg_mask(self, x, y, mask_size):
        """
        Calculates the average value of a square around the map grid position defined by x and y.
        The mask_size defines the size of the square. The calculated mean is then thresholded to
        be either 0 or 100.
        """
        max = int(math.sqrt(mask_size)/2)
        value_sum = 0
        counter = 0
        for cur_x in range(int(x-max),int(x+max),1):
            for cur_y in range(int(y-max),int(y+max),1):
                if cur_y < self.og_map_msg.info.width:
                    if cur_x < self.og_map_msg.info.height:
                        value_sum += self.og_map_msg.data[self.get_map_iter(cur_x, cur_y)]
                        counter +=1

        value_avg = value_sum/counter
        if value_avg >= 50:
            value_final = 100
        else:
            value_final = 0

        return value_final


    def reduce_map(self):
        """
        Creates a new map with a reduced resolution. This is done by combining multiple map values 
        into one by calculating the average value of them and thresholding them to either 100 or 0.
        How much the size of the map is reduced is dependent on self.mask_size which defines
        how many values are used for one value in the new map.
        """
        x=int(math.sqrt(self.mask_size))
        y=int(math.sqrt(self.mask_size))
        self.map = []
        height = 1
        width = 1
        y_counter = 1

        while self.get_map_iter(x,y) < len(self.og_map_msg.data):
            new_value = self.avg_mask(x,y,self.mask_size)
            self.map.append(new_value)

            y += math.sqrt(self.mask_size)
            y_counter += 1

            if y >= self.og_map_msg.info.width:
                width = y_counter-1
                y_counter = 1
                y = int(math.sqrt(self.mask_size))
                x += math.sqrt(self.mask_size)
                height += 1

        self.map_msg.info.width = width
        self.map_msg.info.height = height-1
        #Set resolution of new map
        self.map_msg.info.resolution = self.og_map_msg.info.resolution * math.sqrt(self.mask_size)

        #Print out new size of the map
        self.get_logger().info('New Map Size: '+str(len(self.map)))
        self.map_msg.data = self.map



    def timer_callback(self):
        #-----------------------------------------------------------------------------------
        #TODO: Find the smallest x position on the map grid that has a value of 100 (black)
        #      Repeat the same for: the biggest x position, the smallest y position and the 
        #      biggest y position.
        #      Add those points to the self.marker_msg.points array in these combinations:
        #      - x_min, y_min
        #      - x_min, y_max
        #      - x_max, y_min
        #      - x_max, y_max
        #      NOTE: The marker_msg.points have to be world coordinates not map grid values!
        

        #-----------------------------------------------------------------------------------

        self.pub_filtered_map.publish(self.map_msg)




def main(args=None):
    rclpy.init(args=args)

    map_filter = MapFilterClass()

    rclpy.spin(map_filter)

    map_filter.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()