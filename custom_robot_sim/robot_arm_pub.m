robot_arm_controller_node = ros2node("/robot_arm_matlab_controller", 24);

robot_arm_publisher = ros2publisher(robot_arm_controller_node, "/robot_arm_controller/commands", "std_msgs/Float64MultiArray");
joint_states_subscriber = ros2subscriber(robot_arm_controller_node, "/joint_states", "sensor_msgs/JointState");

zero_pos_msg = ros2message(robot_arm_publisher);
zero_pos_msg.data = [0.0 0.0 0.0 0.0 0.0];

target_pos_msg = ros2message(robot_arm_publisher);
target_pos_msg.data = [pi/4 pi/4 pi/4 pi/4 pi/4];

move_to_target = false;

for cnt = 1:200
    if mod(cnt, 20) == 0
        move_to_target = ~move_to_target;
    end

    receivedData = receive(joint_states_subscriber, 10);
    joint_names = receivedData.name;
    joint_positions = receivedData.position;
    joint_velocities = receivedData.velocity;
    joint_efforts = receivedData.effort;


    if move_to_target
        send(robot_arm_publisher,target_pos_msg);
    else
        send(robot_arm_publisher,zero_pos_msg);
    end
    pause(0.1)
end