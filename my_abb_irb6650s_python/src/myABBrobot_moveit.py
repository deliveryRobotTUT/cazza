import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import gcode_reader

print "============ Starting setup"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface', anonymous=True)

# create objects for using moveit_commander
robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group = moveit_commander.MoveGroupCommander("manipulator")

display_trajectory_publisher = rospy.Publisher(
                                    '/move_group/display_planned_path',
                                    moveit_msgs.msg.DisplayTrajectory)

print "============ Waiting for RVIZ..."
rospy.sleep(10)

# define two empty arrays
waypoints = []
waypoints_defined = []
# get the way-points from "gcode_reader.py"
waypoints_temp = gcode_reader.get_waypoints('Base side 1 rev3.gcode')

for z_pts in range(len(waypoints_temp)):
    # convert readings from mm to m
    z_cord = waypoints_temp[z_pts][0]/1000
    for x_pts in range(len(waypoints_temp[z_pts][1])):
        x_cord = waypoints_temp[z_pts][1][x_pts][0]/1000.0
        y_cord = waypoints_temp[z_pts][1][x_pts][1]/1000.0
        # create another array with orientation and position
        waypoints_defined.append([0.0, 0.866025422, 0.0, 0.499999968, x_cord, y_cord, z_cord])

waypoints.append(group.get_current_pose().pose)

wpose = geometry_msgs.msg.Pose()

for w_pts in waypoints_defined:
    # "empty the array way-points"
    waypoints = []
    # get the orientation and position
    wpose.orientation.w = w_pts[3]
    wpose.orientation.x = w_pts[0]
    wpose.orientation.y = w_pts[1]
    wpose.orientation.z = w_pts[2]
    wpose.position.x = w_pts[4]
    wpose.position.y = w_pts[5]
    wpose.position.z = w_pts[6]
    waypoints.append(copy.deepcopy(wpose))
    # compute trajectory in cartesian space
    (plan1, fraction) = group.compute_cartesian_path(waypoints, 0.1, 0.0)  # jump_threshold
    # execute trajectory
    group.execute(plan1)
    # "empty the array way-points"
    waypoints = []

    print "============ Waiting while RVIZ displays plan1..."
    rospy.sleep(5)

    print "============ Visualizing plan1"
    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan1)
    display_trajectory_publisher.publish(display_trajectory)

    print "============ Waiting while plan1 is visualized (again)..."
    rospy.sleep(5)

