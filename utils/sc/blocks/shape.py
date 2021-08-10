from ..block import ScBlock

from .subs.bitmap import ShapeDrawBitmap



class Shape(ScBlock):
	def __init__(self, tag: int, textures: list):
		super().__init__(tag)
		
		self.textures = textures
	
	def parse(self, data: bytes):
		super().parse(data)
		
		shape = {}
		
		shape["id"] = self.readUShort()
		shape["bitmaps"] = []
		
		self.readUShort() # bitmaps count
		
		if self.tag == 18:
			self.readUShort() # total bitmaps points count
		
		shape["bitmaps"] = self.parse_bitmaps()
		
		return shape
	
	def parse_bitmaps(self):
		bitmaps = []
		
		while True:
			tag = self.readUByte()
			length = self.readUInt32()
			data = self.stream.read(length)
			
			if tag == 0:
				break
			elif tag in [4, 17, 22]:
				bitmap = ShapeDrawBitmap(tag, self.textures)
				bitmaps.append(bitmap.parse(data))
			else:
				print("SupercellSWF::Unknown tag in ShapeDrawBitmapCommand; {} {}".format(tag, length))
		
		return bitmaps
	
	def encode(self, shape: dict):
		super().encode()
		
		self.writeUShort(shape["id"])
		self.writeUShort(len(shape["bitmaps"]))
		
		if self.tag == 18:
			points_count = 0
			for bitmap in shape["bitmaps"]:
				points_count += len(bitmap["points"])
			
			self.writeUShort(points_count)
		
		self.encode_bitmaps(shape["bitmaps"])
		
		self.length = len(self.stream.buffer)
	
	def encode_bitmaps(self, bitmaps: list):
		for bitmap in bitmaps:
			bitmap_data = ShapeDrawBitmap(22, self.textures)
			bitmap_data.encode(bitmap)
			
			self.writeUByte(bitmap_data.tag)
			self.writeUInt32(bitmap_data.length)
			self.stream.write(bitmap_data.stream.buffer)
		
		self.writeUByte(0)
		self.writeUInt32(0)
