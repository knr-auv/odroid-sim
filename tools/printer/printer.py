

class Printer:

    def __init__(self):
        self.motors_value = [0, 0, 0, 0, 0]
        self.roll_value = 0
        self.pitch_value = 0
        self.yaw_value = 0
        self.depth_value = 0

    def print_out(self):
        with open("output.log", "w") as output:
            output.write("L:{}\t{}:P\n\nL:{}\t{}:P\n\n____{}____".format(self.motors_value[0],
                                                                         self.motors_value[1],
                                                                         self.motors_value[2],
                                                                         self.motors_value[3],
                                                                         self.motors_value[4]))
            output.write("\nroll:{}".format(self.roll_value))
            output.write("\npitch:{}".format(self.pitch_value))
            output.write("\nyaw:{}".format(self.yaw_value))
            output.write("\ndepth:{}".format(self.depth_value))

    def set_motors_value(self, motors):
        if len(motors) == 5:
            self.motors_value = motors

    def set_roll(self, roll):
        self.roll_value = roll

    def set_pitch(self, pitch):
        self.pitch_value = pitch

    def set_yaw(self, yaw):
        self.yaw_value = yaw

    def set_depth(self, depth):
        self.depth_value = depth