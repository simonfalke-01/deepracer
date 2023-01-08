import math


def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steps = params['steps']
    progress = params['progress']

    # Thresholds
    SPEED_THRESHOLD = 1.5
    TURNING_SPEED_THRESHOLD = 0.7
    DIRECTION_THRESHOLD = 10.0
    TOTAL_NUM_STEPS = 500

    off_center = 0.6 * track_width

    reward = 1.0

    if not all_wheels_on_track:
        return float(1e-3)

    elif speed < SPEED_THRESHOLD:
        reward = 0.5

    else:
        reward = 1.0

    reward = 1 - (distance_from_center/(track_width/2))**(1/4)

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    direction_diff = abs(track_direction - heading)

    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if direction_diff > DIRECTION_THRESHOLD:
        if speed > TURNING_SPEED_THRESHOLD or distance_from_center <= off_center:
            reward += 0.5

        reward *= 0.5

    if (steps % 50) == 0 and progress / 100 > (steps / TOTAL_NUM_STEPS):
        reward += (progress - (steps / TOTAL_NUM_STEPS) * 100) * 0.8

    return float(reward)
