%% Initialize action client
clc
clear

% Set the ros domain id and create a new ros node
setenv("ROS_DOMAIN_ID","24");
test_node = ros2node("joint_trajectory_client_node");

% Define joint names
joints = { ...
    'arm_base_joint', ...
    'link_1_joint', ...
    'link_2_joint', ...
    'link_3_joint', ...
    'gripper_base_joint', ...
    'gripper_finger_left_joint' };

% Define the action type and name
actionType = "control_msgs/FollowJointTrajectory";
actionName = "/arm_controller/follow_joint_trajectory";


% Create the client
client = ros2actionclient(test_node, actionName, actionType);

disp("Waiting for FollowJointTrajectory action server ...");
waitForServer(client);
disp("Action server available.");

%% Send a joint trajectory goal

% Define a list of goal positions that will define the trajectory
goalPositions = [ ...
    pi/2, pi/2-0.5, 0.4, pi/4, 0.0, -0.05;    % home-ish
    pi/2, pi/2-0.18, 0.6, pi/4, 0.0, -0.05;  % pose 2
    pi/2, pi/2-0.18, 0.6, pi/4, 0.0, -0.02; % pose 3
    pi/2, pi/2-0.5, 0.4, pi/4, 0.0, -0.02;
    -pi/2, pi/2-0.5, 0.6, pi/4, 0.0, -0.02;
    -pi/2, pi/2-0.35, 0.7, pi/4, 0.0, -0.02;
    -pi/2, pi/2-0.35, 0.7, pi/4, 0.0, -0.05;
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0]; % pose 4

% Create a JointTrajectory message object
traj = ros2message("trajectory_msgs/JointTrajectory");
traj.joint_names = joints;

% Add all the previously defined goalPositions to the trajectory as
% JointTrajectoryPoint
for i = 1:size(goalPositions,1)
    pt1 = ros2message("trajectory_msgs/JointTrajectoryPoint");
    pt1.positions      = [goalPositions(i,:)];  % in radians
    pt1.velocities     = zeros(1,6);
    pt1.accelerations  = zeros(1,6);
    pt1.time_from_start.sec = int32(i);
    pt1.time_from_start.nanosec = uint32(0);
    pt1.effort = [];
    pt1.accelerations = [];

    if i == 1
        traj.points = [pt1];
    else
        traj.points = [traj.points, pt1];
    end
end

% Define the goal message using the previously defined trajectory.
goalMsg = ros2message(client);
goalMsg.trajectory = traj;
goalMsg.goal_time_tolerance.sec     = int32(0);
goalMsg.goal_time_tolerance.nanosec = uint32(500000000);  % 0.5 s

% 4. Send goal and monitor
goalHandle = sendGoal(client, goalMsg);

while true
    exStatus = getStatus(client, goalHandle);
    fprintf("Current status: %d\n", exStatus);
    if exStatus == 4 || exStatus == 5 || exStatus == 6
        break;
    end
    pause(0.1);
end

resultMsg = getResult(client, goalHandle);
fprintf("Final status: %d\n", exStatus);

