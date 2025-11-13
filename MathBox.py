import math

# get a delta component (x, y) given a rotation and a speed
# delta x = speed * cos(radian)
# delta y = speed * sin(radian)


# find the direction of the collision on self, use this to reduce armor directionally
# on self during collisions, use magnitude to figure out damage
def find_approach(self_current_direction, self_name,
                  other_current_direction, other_name):
    a = 360 - self_current_direction
    r = a + other_current_direction
    approach = r % 360
    print("self: ", self_name, "other: ", other_name, " approach: ", approach)
    return approach


def get_component_form_from_rotation_magnitude(radian: float, magnitude: int):
    return[(magnitude * math.cos(radian)), (magnitude * math.sin(radian))]


def get_hypotenuse(x, y, window_size):
    mod_x = abs((window_size[0]/2) - x) / 50
    mod_y = abs((window_size[1]/2) - y) / 50
    return math.sqrt((mod_x * mod_x) + (mod_y * mod_y))


def get_x_y_for_given_target_direction_distance(origin, current_speed, direction):
    new_direction = (direction + 180) % 360
    if current_speed < 0:
        x = math.cos(new_direction) * -20
        y = math.sin(new_direction) * 20
    else:
        x = math.cos(new_direction) * 20
        y = math.sin(new_direction) * -20
    print("difference = ", x, y)
    return [origin[0] + x, origin[1] + y]


def get_direction_rotated(origin_x, origin_y, target_x, target_y):
    dx = target_x - origin_x
    dy = target_y - origin_y
    # Swap dx and dy compared to standard formula
    angle_radians = math.atan2(dx, dy)
    angle_degrees = math.degrees(angle_radians)

    # Convert from -180 to 180 range to 0 to 360 if desired
    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees


def find_range(target_x, target_y, origin_x, origin_y):
    x_factor = abs(target_x - origin_x)
    y_factor = abs(target_y - origin_y)
    return math.sqrt((x_factor * x_factor) + (y_factor * y_factor))


def normalize(displacement):
    if displacement < -4:
        return -4
    if displacement > 4:
        return 4
    return displacement


def convert_real_coords_to_map_coords(real_chunk_x, real_chunk_y):
    map_x = real_chunk_x % 15
    if map_x < 0:
       map_x = map_x + 15
    map_y = real_chunk_y % 15
    if map_y < 0:
        map_y = map_y + 15
    return [map_x, map_y]


def getA(display_center_x, item_x):
    return (display_center_x * -1) + item_x


def getB(display_center_y, item_y):
    return (display_center_y * -1) + item_y


def trackz(display_center_x, display_center_y, item_x, item_y):
    xx = getA(display_center_x, item_x)
    yy = getA(display_center_y, item_y)
    return track(xx, yy)


def track(x, y):
    if x > 0 and y < 0:
        return math.atan(y/x)
    if x == 0 and y > 0:
        return math.pi / 2
    if x < 0 and y > 0:
        convert_x = x * -1
        deg = 180 - (math.degrees(math.atan(y/convert_x)) + 90)
        return math.radians(deg + 90)
    if x < 0 and y == 0:
        return math.pi
    if x < 0 and y < 0:
        convert_x = x * -1
        deg = 180 - (math.degrees(math.atan(y / convert_x)) + 90)
        return math.radians(deg + 90)
    if x == 0 and y < 0:
        return (3 * math.pi) / 2
    if x > 0 and y > 0:
        convert_x = x * -1
        deg = 180 - (math.degrees(math.atan(y / convert_x)) + 90)
        return math.radians(deg + 270)
    if x == 0 and y > 0:
        return 2 * math.pi
    return 0


def get_XYOffset_given_direction_offset(direction, offset):
    x_offset = (math.sin(math.radians(direction)) * offset)
    y_offset = (math.cos(math.radians(direction)) * offset)
    return [x_offset, y_offset]


def getRange(x, y):
    return math.sqrt((x * x) + (y * y))


def getX(range, track):
    return range * math.cos(track)


def getY(range, track):
    return range * math.sin(track)


