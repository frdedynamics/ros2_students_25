import rclpy
from rclpy.node import Node
import math
import time

from tf_transformations import euler_from_quaternion
from gazebo_msgs.srv import GetEntityState
from nav_msgs.msg import Odometry
from scoring_interfaces.srv import SetMarkerPosition
from geometry_msgs.msg import Point

class ScoringClass(Node):

    def __init__(self):
        super().__init__('ScoringNode')
        self.inital_positions = [Point(), Point(), Point(), Point(), Point()]
        self.inital_orientations = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.robot_positions = [Point(), Point(), Point(), Point(), Point()]
        self.robot_orientations = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.state = 0
        self.pos_accuracy = 0.5
        self.marker_reported = [False, False, False, False, False]
        self.marker_score = 0
        self.start_time_score = 600
        self.robot_count = 2

        self.create_subscription(Odometry, '/tb3_0/odom', self.clbk_tb3_0_odom, 10)
        self.create_subscription(Odometry, '/tb3_1/odom', self.clbk_tb3_1_odom, 10)
        self.create_subscription(Odometry, '/tb3_2/odom', self.clbk_tb3_2_odom, 10)
        self.create_subscription(Odometry, '/tb3_3/odom', self.clbk_tb3_3_odom, 10)
        self.create_subscription(Odometry, '/tb3_4/odom', self.clbk_tb3_4_odom, 10)

        # Service server definition that is used for reporting found aruco markers
        self.srv = self.create_service(SetMarkerPosition, '/set_marker_position', self.clbk_set_marker_pos)

        # Wait for gazebo to be running
        self.client_entity_state = self.create_client(GetEntityState, '/gazebo/get_entity_state')
        while not self.client_entity_state.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        # Retrieve Marker positions from Gazebo
        self.model_state_markers = []
        for i in range(5):
            new_model_state = self.get_model_state("Marker"+str(i))
            self.get_logger().info("Marker"+str(i)+": "+str(new_model_state.state.pose.position))
            self.model_state_markers.append(new_model_state)

        # Retrieve Robot starting positions from Gazebo
        for i in range(self.robot_count):
            while self.get_model_state("tb3_"+str(i)).state.pose.position.x == 0.0 and self.get_model_state("tb3_"+str(i)).state.pose.position.y == 0.0:
                self.get_logger().info("waiting for turtlebot to spawn")
                time.sleep(1)
            new_robot_state = self.get_model_state("tb3_"+str(i))
            self.inital_positions[i] = new_robot_state.state.pose.position
            self.inital_orientations[i] = self.get_yaw(new_robot_state.state.pose.orientation)
            self.get_logger().info("tb3_"+str(i)+" position: "+str(new_robot_state.state.pose.position))

        self.odom_recieved = [True, True, True, True, True]
        self.start_time = time.time()

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def clbk_set_marker_pos(self, request, response):
        """
        Callback function for the service server
        """
        response.accepted = False
        if request.marker_id < 0 or request.marker_id > 4:
            self.get_logger().error("The reported marker id is not a valid value")
            return response
        if self.state == 5 or self.state == 6:
            self.get_logger().error("The scenario is finished. No more reporting of markers allowed.")
            return response
        x_error = self.model_state_markers[request.marker_id].state.pose.position.x - request.marker_position.x
        y_error = self.model_state_markers[request.marker_id].state.pose.position.y - request.marker_position.y
        z_error = self.model_state_markers[request.marker_id].state.pose.position.z - request.marker_position.z
        distance = math.sqrt(pow(x_error,2)+pow(y_error,2)+pow(z_error,2))
        if distance < self.pos_accuracy:
            if self.marker_reported[request.marker_id] == False:
                self.marker_reported[request.marker_id] = True
                response.accepted = True
                if request.marker_id == 0 or request.marker_id == 1 or request.marker_id == 3:
                    self.marker_score += 100
                elif request.marker_id == 2:
                    self.marker_score += 100
                elif request.marker_id == 4:
                    self.marker_score += 100
        else:
            self.get_logger().error("The reported position for marker "+str(request.marker_id)+"is inaccureate. The allowed accuracy is "+str(self.pos_accuracy))
            return response

        return response

                
    def get_yaw(self, orientation):
        """
        Transfroms quaternion orientation into euler angles and returns the yaw (rotation around z axis) value
        """
        quaternion = (
            orientation.x,
            orientation.y,
            orientation.z,
            orientation.w)
        euler = euler_from_quaternion(quaternion)
        yaw = euler[2]

        return yaw

    def clbk_tb3_0_odom(self, msg):
        self.robot_positions[0] = msg.pose.pose.position
        self.robot_orientations[0] = self.get_yaw(msg.pose.pose.orientation)

    def clbk_tb3_1_odom(self, msg):
        self.robot_positions[1] = msg.pose.pose.position
        self.robot_orientations[1] = self.get_yaw(msg.pose.pose.orientation)
    
    def clbk_tb3_2_odom(self, msg):
        self.robot_positions[2] = msg.pose.pose.position
        self.robot_orientations[2] = self.get_yaw(msg.pose.pose.orientation)

    def clbk_tb3_3_odom(self, msg):
        self.robot_positions[3] = msg.pose.pose.position
        self.robot_orientations[3] = self.get_yaw(msg.pose.pose.orientation)

    def clbk_tb3_4_odom(self, msg):
        self.robot_positions[4] = msg.pose.pose.position
        self.robot_orientations[4] = self.get_yaw(msg.pose.pose.orientation)

    def get_model_state(self, model_name):
        """
        Returns state information about a model from gazebo using the models name
        """
        req = GetEntityState.Request()
        req.name = model_name
        self.future = self.client_entity_state.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
    def check_robot_movement(self):
        """
        Check if any of the robots are moved by more than 0.1 meters or radian
        """
        linear_movement_thresh = 0.1
        angular_movement_thresh = 0.1

        for i in range(len(self.inital_positions)):
            if self.odom_recieved[i]:
                delta_x = abs(self.inital_positions[i].x - self.robot_positions[i].x)
                delta_y = abs(self.inital_positions[i].y - self.robot_positions[i].y)
                delta_yaw = abs(self.inital_orientations[i] - self.robot_orientations[i])

                if delta_x > linear_movement_thresh or delta_y > linear_movement_thresh or delta_yaw > angular_movement_thresh:
                    self.get_logger().info("delta_x: "+str(delta_x)+", delta_y: "+str(delta_y)+", delta_yaw: "+str(delta_yaw))
                    self.start_time = time.time()
                    return True

        return False

    def check_big_fire_proximity(self):
        """
        Checks how many robots are within a 2 meter proximity of the marker with id 4
        """
        robot_cntr = 0
        for robot_pos in self.robot_positions:
            x_error = self.model_state_markers[4].state.pose.position.x - robot_pos.x
            y_error = self.model_state_markers[4].state.pose.position.y - robot_pos.y
            distance = math.sqrt(pow(x_error,2)+pow(y_error,2))
            if distance < 2.0:
                robot_cntr += 1

        if robot_cntr >= 2:
            return True
        
        return False

    
    def report_score(self):
        """
        Calculates the current and final score
        """

        if self.state == 5:
            elapsed_time = int(self.finish_time - self.start_time)
        elif self.state == 6:
            elapsed_time = 600
        else:
            elapsed_time = int(time.time() - self.start_time)
            if elapsed_time > 600:
                self.state = 6

        score = self.start_time_score - elapsed_time + self.marker_score

        if self.state == 5 or self.state == 6:
            self.get_logger().info("Final Score: "+str(score))
        else:
            self.get_logger().info("Score: "+str(score))
    
    def timer_callback(self):
        """
        Timer function that is exectued every 0.5 seconds
        """
        if self.state == 0:
             #state 0 - wait for getting the intial positions and orientations of at least tb3_0 and tb3_1
            if self.odom_recieved[0] and self.odom_recieved[1]:
                self.get_logger().info("Initial Positions recieved: "+str(self.inital_positions))
                self.state = 1
        
        elif self.state == 1:
            #state 1 - waiting for the robot's to start moving
            if self.check_robot_movement():
                self.state = 2
        
        elif self.state == 2:
            #state 2 - waiting for the roporting of big fire
            if self.marker_reported[4]:
                self.state = 3
        
        elif self.state == 3:
            #state 3 - checking robot position for proximity of the big fire ar tag
            if self.check_big_fire_proximity():
                self.marker_score += 300
                self.state = 4
        
        elif self.state == 4:
            #state 4 - wait for all ar tags to be found
            markers_found = True
            for marker in self.marker_reported:
                if not marker:
                    markers_found = False

            if markers_found:
                self.finish_time = time.time()
                self.state = 5

        if self.state > 1:
            self.report_score()



def main(args=None):
    rclpy.init(args=args)

    scoring_object = ScoringClass()

    rclpy.spin(scoring_object)
    scoring_object.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()