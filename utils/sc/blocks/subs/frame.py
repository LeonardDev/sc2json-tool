from ...block import ScBlock



class MovieFrame(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		transforms_count = self.readUShort()
		frame_name = self.readString()
		
		return {
				"name": frame_name,
				"count": transforms_count
		}
	
	def encode(self, frame: dict):
		super().encode()
		
		self.writeUShort(frame["count"])
		self.writeString(frame["name"])
		
		self.length = len(self.stream.buffer)
