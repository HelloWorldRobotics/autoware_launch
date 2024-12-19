# Autoware Configuration Changes

This document outlines all behavioral changes made to Autoware configuration files.

## Operation Mode Transition Manager
- 🟢 **Enable engage while driving**: `enable_engage_on_driving: true`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: To be able to switch to auto drive when moving [NOT TESTED PROPERLY]</span>

- 🟢 **Speed thresholds modified**:
  ```yaml
  speed_upper_threshold: 2.0
  speed_lower_threshold: -2.0
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: To be able to switch to auto drive when moving [NOT TESTED PROPERLY]</span>

## Longitudinal PID Controller
- 🟢 **Delay compensation**: `delay_compensation_time: 0.25`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Compensate delay in buggy control</span>

- 🟢 **Emergency flags**: `enable_overshoot_emergency: false`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Disable unnecessary emergency flags</span>

- 🟢 **Slope handling**: 
  ```yaml
  enable_slope_compensation: false
  enable_keep_stopped_until_steer_convergence: false
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Unreliable slope sources currently due to lanelet/PCD [FUTURE: TEST WITH IMU SLOPE]</span>
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: To switch to auto faster</span>

- 🟢 **Stop distances increased**:
  ```yaml
  drive_state_stop_dist: 2.0
  stopping_state_stop_dist: 2.0
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Increased since no brake implemented yet</span>

- 🟢 **PID parameters tuned**:
  ```yaml
  kp: 0.2
  ki: 0.001
  kd: 0.2
  max_out: 0.2
  max_p_effort: 0.2
  min_p_effort: -0.2
  max_i_effort: 0.05
  min_i_effort: -0.05
  max_d_effort: 0.2
  min_d_effort: -0.2
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Tested appropriate values</span>

- 🟢 **Integration threshold**: `current_vel_threshold_pid_integration: 2.0`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Increased since no brake implemented yet</span>

- 🟢 **Stop acceleration values**:
  ```yaml
  smooth_stop_max_strong_acc: -2.5
  smooth_stop_min_strong_acc: -2.0
  smooth_stop_weak_acc: -2.0
  smooth_stop_weak_stop_acc: -2.0
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Increased since no brake implemented yet</span>

- 🟢 **Maximum acceleration**: `max_acc: 0.5`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Stop in time, no brakes, this is the max accel we can expect</span>

## Map Based Prediction
- 🟢 **Unknown object prediction**: `unknown: 1.0`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Increase unknown path prediction accuracy</span>

## Ground Segmentation
- 🟢 **Ground segmentation parameters optimized**:
  ```yaml
  local_slope_max_angle_deg: 25.0
  split_points_distance_tolerance: 0.3
  use_virtual_ground_point: true
  split_height_distance: 0.05
  non_ground_height_threshold: 0.15
  detection_range_z_max: 1.0
  elevation_grid_mode: false
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Better ground segmentation, tested</span>

## Default Preset
- 🟢 **Dynamic obstacle avoidance**: `launch_dynamic_obstacle_avoidance: "true"`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Activate disabled detection module</span>

- 🟢 **Speed bump module**: `launch_speed_bump_module: "true"`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Slow down for speedbump</span>

## Velocity Smoother
- 🟢 **Lateral acceleration parameters**:
  ```yaml
  max_lateral_accel: 0.65
  min_curve_velocity: 0.8
  decel_distance_before_curve: 5.5
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Appropriate cornering speeds tested</span>

- 🟢 **Engage velocity**: `engage_velocity: 0.5`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Appropriate engage velocity to start</span>

- 🟢 **Stopping parameters**:
  ```yaml
  stopping_velocity: 0.5
  stopping_distance: 2.0
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Slow down for stopping</span>
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Slow down earlier for stopping</span>

## Common Planning Parameters
- 🟢 **Acceleration and jerk limits**:
  ```yaml
  min_acc: -0.4
  min_jerk: -0.25
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: No brake deceleration</span>
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: No brake jerk deceleration</span>

## Planning Validator
- 🟢 **Invalid trajectory handling**: `invalid_trajectory_handling_type: 2`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Attempt to continue on invalid trajectory [NOT TESTED]</span>

- 🟢 **Trajectory margin**: `forward_trajectory_length_margin: 3.0`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Longer trajectory to avoid stopping</span>

## Dynamic Obstacle Avoidance
- 🟢 **Obstacle velocity threshold**: `min_obstacle_vel: 1.0`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Dont consider stopped objects</span>

- 🟢 **Lateral offset**: `lat_offset_from_obstacle: 0.3`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Cars are crazy here so if its not small we will be avoiding all the time</span>

- 🟢 **Pedestrian margin**: `margin_distance_around_pedestrian: 0.6`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Changed when tuning before GPU install with all unknown object params</span>

## Static Obstacle Avoidance
- 🟢 **Lateral margins**:
  ```yaml
  soft_margin: 0.5
  hard_margin_for_parked_vehicle: 0.3
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: More room when avoiding static obstacles</span>
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: More room when avoiding parked vehicles</span>

## Speed Bump Parameters
- 🟢 **Speed bump approach**: 
  ```yaml
  slow_start_margin: 2.0
  slow_end_margin: 0.5
  max_speed: 2.30
  ```
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: More room when stopping at speed bump</span>
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Accel faster after stopping at speed bump</span>
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Slower speed</span>

## Stop Line Parameters
- 🟢 **Stop margin**: `stop_margin: 2.0`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Stop in time, no brakes</span>

## Path Optimizer
- 🟢 **Drivable area check**: `enable_outside_drivable_area_stop: false`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Required for lane change by avoidance</span>

## Freespace Planner
- 🟢 **Parking velocity**: `waypoints_velocity: 1.0`
  - <span style="color:orange">TO GET DESIRED BEHAVIOR: Slower speed when parking</span>

---
**Note**: Parameters marked with 🟢 have been tested and verified. Some changes are temporary solutions until hardware improvements are implemented.