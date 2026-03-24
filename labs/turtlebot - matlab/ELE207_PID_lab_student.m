%% ELE207 turtlebot lab

clear all;
clc;
close all;
%% Setting up the ROS environment 
setenv("ROS_DOMAIN_ID","30");
setenv("ROS_IP", "172.31.1.101"); % your windows PC's IP adress 

% Initializing ros node
pidControllerNode = ros2node("/pid_controller");

% Creating subscriber to laser scan and publisher to cmd velocity
pause(3)
laserSub = ros2subscriber(pidControllerNode,"/scan","sensor_msgs/LaserScan","Reliability","besteffort","Durability","volatile","Depth",5);
cmdvalPub = ros2publisher(pidControllerNode, "/cmd_vel", "geometry_msgs/Twist");
pause(3)

% Defining message for publisher
cmdvelMsg = ros2message(cmdvalPub);

%% Defining variables

% Front left and front right distances
lidar_left_front = 0;
lidar_right_front = 0;

% Front left and front right angles - you can tweak those if you dissagree
left_range = 40; % 40 degrees to the left
right_range = 320; % 40 degrees to the right

% Targer distance - TODO: tweak those variables!
target_dist = 0.35; % In meters, the desired distance between the wall and the center of the lidar, should be tweaked too
too_close_dist = 0.2; % In meters, this should also be tweaker
%% PID Controller

% PID params - TODO: tweak the gains of the PID controller to get the
% desired controller
Kp = 1.2;               
Ki = 0.01;              
Kd = 0.2;               

% Variables used in the PID controller
prev_error = 0;
integral = 0;
dt = 0.01;               

%% Controlling the turtlebot
% For ever loop
while true
    % Reading out the scan data 
    [scanData,status,statustext] = receive(laserSub, 10);
    lidar_left_front = scanData.ranges(left_range);
    lidar_right_front = scanData.ranges(right_range);

    % Calculating based on the min distance to the wall on the left side
    % LIDAR detection distance: 120mm ~ 3,500mm 
    % https://emanual.robotis.com/docs/en/platform/turtlebot3/appendix_lds_01/
    current_dist = min(scanData.ranges(left_range)); % compute the average over some points/angles for a better result
    
    % Calculate Error - TODO
    dist_error = ;
    disp("Error:")
    disp(dist_error)
    
    % Calculating the PID terms based on the error - TODO
    P = ;

    integral = ;
    I = ;
    
    derivative = ;
    D = ;
    
    % Combining control outputs 
    angular_vel = -double(P + I + D);
    
    % Setting up the velocity
    cmdvelMsg.linear.x = 0.1;
    cmdvelMsg.angular.z = angular_vel;
    disp("angular_vel:");
    disp(angular_vel)

    % Safety: If too close, stop
    if current_dist < too_close_dist
        cmdvelMsg.linear.x = 0.001;
        disp("Too close!")
    end

    % Plotting the scan data for fun and debbuging
    angles = linspace(-pi, pi, 360);
    scan = lidarScan(scanData.ranges, angles);
    all_points = scan.Cartesian; % This is a [360 x 2] matrix
    left_range_points = all_points(left_range, :);
    hold off;
    % Plot everything else in small blue dots
    plot(all_points(:,1), all_points(:,2), 'b.', 'MarkerSize', 4); 
    hold on;
    % Except for the point we calculate the distance - it's red 
    plot(left_range_points(:,1), left_range_points(:,2), 'r.', 'MarkerSize', 12);
    
    % Keeping the plot
    axis equal;
    grid on;
    xlabel('X (meters)');
    ylabel('Y (meters)');
    legend('Full Scan', 'Left Range');

   
    % Send velocity commands to turtlebot
    send(cmdvalPub, cmdvelMsg)

    % Save state for next iteration
    prev_error = dist_error;
    pause(dt);
    
end


