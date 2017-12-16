import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import gcode_reader

print "============ Starting tutorial setup"
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group = moveit_commander.MoveGroupCommander("manipulator")

# velocity = moveit_commander.

display_trajectory_publisher = rospy.Publisher(
                                    '/move_group/display_planned_path',
                                    moveit_msgs.msg.DisplayTrajectory)

print "============ Waiting for RVIZ..."
rospy.sleep(5)
print "============ Starting tutorial "

print "============ Reference frame: %s" % group.get_planning_frame()

print "============ Generating plan 1"
pose_target = geometry_msgs.msg.Pose()
pose_target.orientation.x = -8.06293423223e-05
pose_target.orientation.y = 0.70715645205
pose_target.orientation.z = -3.74177349839e-05
pose_target.orientation.w = 0.707057101246
pose_target.position.x = 2.0
pose_target.position.y = 0.0
pose_target.position.z = 1.0
group.set_pose_target(pose_target)

plan1 = group.plan()
group.execute(plan1, True)
print "plan executed"
# waypoints = []
# waypoints_defined = []
# waypoints_temp = gcode_reader.get_waypoints('Base side 1 rev3.gcode')
# # print (waypoints_temp)
# for z_pts in range(len(waypoints_temp)):
#     z_cord = waypoints_temp[z_pts][0]/1000
#     # print len(waypoints_temp[z_pts][1])
#     for x_pts in range(len(waypoints_temp[z_pts][1])):
#         # print waypoints_temp[z_pts][1][x_pts][0]
#         x_cord = waypoints_temp[z_pts][1][x_pts][0]/1000.0
#         y_cord = waypoints_temp[z_pts][1][x_pts][1]/1000.0
#         waypoints_defined.append([0.0, 0.866025422, 0.0, 0.499999968, x_cord, y_cord, z_cord])
#
# waypoints.append(group.get_current_pose().pose)
# # print waypoints
# # print group.get_current_joint_values()
# wpose = geometry_msgs.msg.Pose()
# # print wpose
#
# for w_pts in waypoints_defined:
#     print w_pts
#     wpose.orientation.w = w_pts[3]
#     wpose.orientation.x = w_pts[0]
#     wpose.orientation.y = w_pts[1]
#     wpose.orientation.z = w_pts[2]
#     wpose.position.x = w_pts[4]
#     wpose.position.y = w_pts[5]
#     wpose.position.z = w_pts[6]
#     waypoints.append(copy.deepcopy(wpose))
#     # print waypoints
#     (plan1, fraction) = group.compute_cartesian_path(waypoints, 0.1, 0.0)  # jump_threshold
#     group.execute(plan1)
#
#     waypoints = []
#
#     print "============ Waiting while RVIZ displays plan1..."
#     rospy.sleep(5)
#
#     print "============ Visualizing plan1"
#     display_trajectory = moveit_msgs.msg.DisplayTrajectory()
#
#     display_trajectory.trajectory_start = robot.get_current_state()
#     display_trajectory.trajectory.append(plan1)
#     display_trajectory_publisher.publish(display_trajectory)
#
#     print "============ Waiting while plan1 is visualized (again)..."
#     rospy.sleep(5)

