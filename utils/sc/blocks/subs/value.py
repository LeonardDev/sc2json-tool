from ...block import ScBlock



class MovieValue(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		return self.readByte()
	
	def encode(self, value: int):
		super().encode()
		
		self.writeByte(value)
		
		self.length = len(self.stream.buffer)
