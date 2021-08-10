from ...block import ScBlock



class ShapeRegion(ScBlock):
	def __init__(self, tag: int, textures: list):
		super().__init__(tag)
		
		self.textures = textures
	
	def parse(self, data: bytes):
		super().parse(data)
		
		region = {}
		
		region["textureIndex"] = self.readUByte()
		
		region["points"] = []
		
		points_count = 4
		if self.tag != 4:
			points_count = self.readUByte()
		
		for i in range(points_count):
			# twips XY
			x = self.readInt32() / 20
			y = self.readInt32() / 20
			
			region["points"].append({
				"output": [x, y],
				"uv": [0, 0]
			})
		
		for i in range(points_count):
			# texture UV
			u = self.readUShort()
			v = self.readUShort()
			
			if self.tag == 22:
				u /= 65535
				v /= 65535
				
				u *= self.textures[region["textureIndex"]]["width"]
				v *= self.textures[region["textureIndex"]]["height"]
			
			region["points"][i]["uv"] = [round(u), round(v)]
		
		return region
	
	def encode(self, region: dict):
		super().encode()
		
		self.writeUByte(region["textureIndex"])
		self.writeUByte(len(region["points"]))
		
		for point in region["points"]:
			x = point["output"][0] * 20
			y = point["output"][1] * 20
			
			self.writeInt32(round(x))
			self.writeInt32(round(y))
		
		for point in region["points"]:
			u = point["uv"][0]
			v = point["uv"][1]
			
			if self.tag == 22:
				u *= 65535
				v *= 65535
				
				u /= self.textures[region["textureIndex"]]["width"]
				v /= self.textures[region["textureIndex"]]["height"]
			
			self.writeUShort(round(u))
			self.writeUShort(round(v))
		
		self.length = len(self.stream.buffer)
