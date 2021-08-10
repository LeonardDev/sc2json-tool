from ..block import ScBlock



class Modifier(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		modifier = {}
		
		modifier["modifierType"] = self.tag
		modifier["modifierValue"] = self.readUShort()
		
		return modifier
	
	def encode(self, modificator: dict):
		super().encode()
		
		self.writeUShort(modificator["modifierValue"])
		
		self.length = len(self.stream.buffer)
