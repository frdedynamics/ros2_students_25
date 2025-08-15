%% ELE306 turtlebot lab number 1
clc; 
clear; 
close all;

% Setting up the environment: you have to define YOUR ros domain id 

% Initializing a ros node


% Creating subscriber to laser scan (you will need those key words "Reliability","besteffort","Durability","volatile","Depth" ) and publisher to cmd velocity
pause(3)
% here!
pause(3)

% Defining the message type for the publisher


% Defining variables

% Front left and front right distances
lidar_left_front = 0;
lidar_right_front = 0;

% Front left and front right angles
left_range = ;
right_range = ;

% Distance threshold
lidar_threshold = ;

% For ever loop
while true
    % Reading out the scan data 
    

    % Plotting the scan data for fun :)
    angles = linspace(-pi,pi,360);
    scan = lidarScan(scanData.ranges, angles);
    plot(scan);
    
    % Velocity commands if no obstacle


    % Velocity commands if obstacles on both sides
    if 
       
    else
        % Velocity commands if obstacles on the right side -> turning left
        if 
        
        end 
        % Velocity commands if obstacles on the left side -> turning right
        if 
        
        end
    end 
    % Send velocity commands to turtlebot
   
end
