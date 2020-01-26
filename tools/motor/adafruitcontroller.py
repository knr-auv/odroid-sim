import time
from .motorcontroller import MotorController


class AdafruitController(MotorController):

	def __init__(self, config):
		super().__init__(config)

		import Adafruit_PCA9685
		self._set_frequency(config.get("frequency"))

		self.pwm = Adafruit_PCA9685.PCA9685()
		self.pwm.set_pwm_freq(config.get("frequency"))

	def _set_frequency(self, freq):
		self.frequency = freq
		pulse = 1000. / freq	#in ms
		if self.max_pulse < pulse:
			self.min_duty = round(self.min_pulse / pulse * 4096.)
			self.mid_duty = round(self.mid_pulse / pulse * 4096. - 1)
			self.max_duty = int(self.max_pulse / pulse * 4096. - 1)

	def print_duties(self):
		print(self.min_duty, self.mid_duty, self.max_duty)
	
	def _initialize_all(self):
		print('--Preparing motors--')
		for i in range(5):
			self._initialize_motor(i)
		print('---Motors are ready!---')
		time.sleep(1)

	def _initialize_motor(self, motor_num):
		self.pwm.set_pwm(motor_num, 0, self.mid_duty)
		time.sleep(1)

	def _run_motor(self, motor_num, speed):
		duty = self._map_speed(speed)
		#print(duty / 4095 * 1000. / self.frequency)
		self.pwm.set_pwm(motor_num, 0, int(duty))

	def stop_all(self):
		for i in range(5):
			self.run_motor(i, 0)

	def _map_speed(self, speed):
		if speed > self.max_speed:
			return self.max_duty

		if speed < self.min_speed:
			return self.min_speed

		return round((speed - self.min_speed) * (self.max_duty - self.min_duty) / (self.max_speed - self.min_speed) + self.min_duty)

	def _map_motor(self, motor_num):
		if motor_num == 0:
			return 15
		elif motor_num == 1:
			return 14
		elif motor_num == 2:
			return 13
		elif motor_num == 3:
			return 12
		elif motor_num	== 4:
			return 11
		else:
			return 10
