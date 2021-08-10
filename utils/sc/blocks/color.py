from ..block import ScBlock



class ColorTransform(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		color = {}
		
		# Color addition
		blueAdd = self.readNUByte()
		greenAdd = self.readNUByte()
		redAdd = self.readNUByte()
		color["rgbAdd"] = [redAdd, greenAdd, blueAdd]
		
		# Color multipliers
		alphaMul = self.readNUByte()
		blueMul = self.readNUByte()
		greenMul = self.readNUByte()
		redMul = self.readNUByte()
		color["rgbaMul"] = [redMul, greenMul, blueMul, alphaMul]
		
		return color
	
	def encode(self, color: dict):
		super().encode()
		
		self.writeNUByte(color["rgbAdd"][2])
		self.writeNUByte(color["rgbAdd"][1])
		self.writeNUByte(color["rgbAdd"][0])
		
		self.writeNUByte(color["rgbaMul"][3])
		self.writeNUByte(color["rgbaMul"][2])
		self.writeNUByte(color["rgbaMul"][1])
		self.writeNUByte(color["rgbaMul"][0])
		
		self.length = len(self.stream.buffer)
