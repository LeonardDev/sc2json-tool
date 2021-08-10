from ...block import ScBlock



class ShapeDrawBitmap(ScBlock):
	def __init__(self, tag: int, textures: list):
		super().__init__(tag)
		
		self.textures = textures
	
	def parse(self, data: bytes):
		super().parse(data)
		
		bitmap = {}
		
		bitmap["textureIndex"] = self.readUByte()
		
		bitmap["isRectangle"] = False
		if self.tag == 4:
			bitmap["isRectangle"] = True
			points_count = 4
		else:
			points_count = self.readUByte()
		
		bitmap["points"] = []
		
		for i in range(points_count):
			# twips XY
			x = self.readInt32() / 20
			y = self.readInt32() / 20
			
			bitmap["points"].append({
				"twip": [x, y],
				"uv": [0, 0]
			})
		
		for i in range(points_count):
			# texture UV
			u = self.readUShort()
			v = self.readUShort()
			
			if self.tag == 22:
				u /= 65535
				v /= 65535
				
				u *= self.textures[bitmap["textureIndex"]]["width"]
				v *= self.textures[bitmap["textureIndex"]]["height"]
			
			bitmap["points"][i]["uv"] = [round(u), round(v)]
		
		return bitmap
	
	def encode(self, bitmap: dict):
		super().encode()
		
		self.writeUByte(bitmap["textureIndex"])
		
		if not bitmap["isRectangle"]:
			self.writeUByte(len(bitmap["points"]))
		
		for point in bitmap["points"]:
			x = point["twip"][0] * 20
			y = point["twip"][1] * 20
			
			self.writeInt32(round(x))
			self.writeInt32(round(y))
		
		for point in bitmap["points"]:
			u = point["uv"][0]
			v = point["uv"][1]
			
			if self.tag == 22:
				u *= 65535
				v *= 65535
				
				u /= self.textures[bitmap["textureIndex"]]["width"]
				v /= self.textures[bitmap["textureIndex"]]["height"]
			
			self.writeUShort(round(u))
			self.writeUShort(round(v))
		
		self.length = len(self.stream.buffer)
