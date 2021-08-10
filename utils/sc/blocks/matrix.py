from ..block import ScBlock

from math import *



class Matrix(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		# 2x2 transformation matrix
		v1_1 = self.readInt32() / 1024
		v2_1 = self.readInt32() / 1024
		v1_2 = self.readInt32() / 1024
		v2_2 = self.readInt32() / 1024
		
		# twip XY
		x = self.readInt32() / 20
		y = self.readInt32() / 20
		
		return [
			[v1_1, v1_2, x],
			[v2_1, v2_2, y]
		]
	
	def encode(self, matrix: list):
		super().encode()
		
		self.writeInt32(round(matrix[0][0] * 1024))
		self.writeInt32(round(matrix[1][0] * 1024))
		self.writeInt32(round(matrix[0][1] * 1024))
		self.writeInt32(round(matrix[1][1] * 1024))
		
		self.writeInt32(round(matrix[0][2] * 20))
		self.writeInt32(round(matrix[1][2] * 20))
		
		self.length = len(self.stream.buffer)
