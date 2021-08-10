from ..block import ScBlock



class TextureSWF(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		texture = {}
		
		texture["pixelType"] = self.readUByte()
		
		texture["width"] = self.readUShort()
		texture["height"] = self.readUShort()
		
		return texture
	
	def encode(self, texture: dict):
		super().encode()
		
		self.writeUByte(texture["pixelType"])
		
		self.writeUShort(texture["width"])
		self.writeUShort(texture["height"])
		
		self.length = len(self.stream.buffer)
