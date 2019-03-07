import numpy as np

class Position:
	def __init__(self, length=10, precision=2):
		self.length = length
		self.precision = precision

		self.x = []
		self.y = []

	def update_position(self, x, y):
		self.x = [round(x, self.precision)] + self.x[0:self.length-1]
		self.y = [round(y, self.precision)] + self.y[0:self.length-1]

	def get_position(self):
		average = self.__moving_average()
		return np.array(average) if average is not None else None

	def remove_last(self):
		self.x = self.x[:-1]
		self.y = self.y[:-1]

	def __moving_average(self):
		if len(self.x) == 0:
			return None
		return sum(self.x) / len(self.x), sum(self.y) / len(self.y)
