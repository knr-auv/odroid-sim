PAD_STEERING_FLAG = False

SAVE_FLAG = False
READ_FLAG = False
MOVES_FILE = "moves.dat"

CSV_FLAG = False


IP_ADDRESS_2 = '10.41.0.4'  # address jetson
IP_ADDRESS_1 = '192.168.137.208'  # address odroid

PAD_PORT = 8186

RUN_FORWARD_VALUE = 0

# horizontal left / right, vertical left/mid/right
motors_names = ['hl', 'hr', 'vl', 'vm', 'vr']   # should be connected in this order to pwm outputs 0, 1, 2,...
# ML, MR, FL, B, FR in simulation

# list where motors' speeds will be stored
motors_speed = [0, 0, 0, 0, 0]

# list of changes to motors' speeds made by PIDs
motors_speed_diff_pid = [0, 0, 0, 0, 0]

# list of changes to motors' speeds made by pad
motors_speed_pad = [0, 0, 0, 0, 0]

# roll, pitch, yaw angles
RPY_angles = [0, 0, 0]

run_flag = False