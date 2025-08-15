%% ELE306 turtlebot lab number 2
clc; 
clear; 
close all;
import ETS3.*

%% Environment setup
% Setting up environment: you have to define YOUR ros domain id


% Initializing ros node, with a name that makes sense

pause(2)
% Creating publisher to /arm_controller/joint_trajector, message type being trajectory_msgs/JointTrajectory

pause(3)


% Defining message for publisher, and joint_names component


%% Defining the robotic arm
L1 = ;
L2 = ;
L3 = ;
L4 = ;
L5 = ;
L6 = sqrt(L2*L2 + L3*L3);
beta = atan(L3/L2);


%j1 = Revolute('d', ?, 'a', ?, 'alpha', pi/2, 'offset', pi);
%j2 = Revolute('d', ?, 'a', ?, 'alpha', 0, 'offset', beta + pi/2);
%j3 = Revolute('d', ?, 'a', ?, 'alpha', 0, 'offset', -beta + pi/2);
%j4 = Revolute('d', ?, 'a', ?, 'alpha', 0, 'offset', 0);

robot = SerialLink([j1 j2 j3 j4],'name', 'my robot');
robot.qlim = [-3.14, +3.14; -1.57, +1.57; -1.40, +1.57; -1.57, 1.57];

% Visualizing the arm on zero position to check that the definition is correct
robot.plot([0, 0, 0, 0]);

%% Control the gripper and make sure it's open
% Create a publisher for /simple_gripper_cmd with topic type std_msgs/Float64


% Make sure the gripper is open  /simple_gripper_cmd => 0.0


%% Time for inverse kinematics!

% First position:

% Define a goal in the reference frame of the base of the arm, with orientation!

% Apply inverse kinematics which TAKE INTO ACCOUNT JOINT LIMITS! and an initial position

% Check the result with plot

% Create a publisher message with that goal in joint space


% Do that as many times as needed to get the full trajectory of the arm and then send the message with all positions


%% Gripping an object
% Create a new gripper goal and send it


%% Taking the object up, for safe keeping
% Reproduce what was done before to control the arm and fold it back in a safe way where it can store the cup while it navigates the maze




%%
% Function definitions at the end if needed
