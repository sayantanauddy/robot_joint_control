% Script to compute the behavior of a single joint driven by a set of
% neural Matsuoka oscillators

clearvars;
clearvars -global;

% Name of joint
global jointname;
jointname = 'RShoulderPitch';

% Setup the python module
if count(py.sys.path,'') == 0
    insert(py.sys.path,int32(0),'');
end
mod = py.importlib.import_module('nao');
py.reload(mod);

% Initialize the joint (in degrees)
py.nao.setJointAngle(jointname,0.0,1.0);

% Oscillator constants
global t1;
global t2;
global beta;
global eta;
global sigma;
global h_psi;
T = 2.0; % Time period of joint oscillation
t1 = 2.13 + 0.6804*T - sqrt(4.512 + 2.685*T);
t2 = 2.5*t1;
beta = 2.5;
eta = 2.5;
sigma = 1.5;
h_psi = 5.0;

% State variables of the oscillator
global psi_i;
global psi_j;
global phi_i;
global phi_j;
global u_i;
global u_j;
psi_i = 0.0;
psi_j = 1.0;
phi_i = 0.0;
phi_j = 1.0;
u_i = 1.5;
u_j = 1.5;

% Mean position of oscillation of the joint angle
global theta_star;
theta_star = 0.0;

% Variables required to calculate the time delta
global time_prev;
global time_now;
time_prev = 0;
time_now = 0;

% List used for plotting the torques
global torque_list;
torque_list = [];

% List for average position
global avg_position;
avg_position = [];

% Set the time steps
t = [0:0.1:30];

% Solve the differential equations of the inertial mechanical system
% Use custom ODE solver which uses fixed time steps
% Matlab's in-built ODE solver uses variable time steps and sometimes goes
% back in time to adjust the time step. This causes problems in the state
% variables of the matsuoka oscillator.
y=ode1(@inertial_ode,t,[0; 0]);


% Plot the results

hold on;
plot(1);
p1 = plot(t,y(:,1),'b');
p2 = plot(t,avg_position,'r');
p1(1).LineWidth = 2;
p2(1).LineWidth = 2;
xlabel('time (s)');
ylabel('joint angle (rad)');
set(gca,'fontsize',20);
legend([p1,p2],'joint angle', 'average position');

figure;
plot(2);
hold on;
p3 = plot(t,torque_list);
p3(1).LineWidth = 2;
legend([p3],'torque','g');
xlabel('time (s)');
ylabel('torque (Nm)');
set(gca,'fontsize',20);
hold off;
