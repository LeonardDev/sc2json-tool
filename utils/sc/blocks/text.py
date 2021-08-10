from ..block import ScBlock



class TextField(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		text = {}
		
		text["id"] = self.readUShort()
		
		text["fontName"] = self.readString()
		text["rgbaCol"] = [self.readNUByte() for x in range(4)]
		
		text["unknownBool1"] = self.readBool()
		text["unknownBool2"] = self.readBool()
		text["unknownBool3"] = self.readBool()
		text["unknownBool4"] = self.readBool()
		
		text["unknownByte1"] = self.readByte()
		text["unknownByte2"] = self.readByte()
		
		text["unknownShort1"] = self.readShort()
		text["unknownShort2"] = self.readShort()
		text["unknownShort3"] = self.readShort()
		text["unknownShort4"] = self.readShort()
		
		text["unknownBool5"] = self.readBool()
		
		text["text"] = self.readString()
		if self.tag == 7:
			return text
		
		text["extra"] = {}
		extra = text["extra"]
		
		extra["unknownBool6"] = self.readBool()
		if self.tag in [21, 25, 33, 44]:
			extra["rgbaCol"] = [self.readNUByte() for x in range(4)]
		elif self.tag == 20:
			return text
		
		if self.tag in [33, 44]:
			extra["unknownShort5"] = self.readShort()
			extra["unknownShort6"] = self.readShort()
			
			if self.tag == 44:
				extra["unknownShort7"] = self.readShort()
				extra["unknownBool7"] = self.readBool()
		
		return text
	
	def encode(self, text: dict):
		super().encode()
		
		self.writeUShort(text["id"])
		
		self.writeString(text["fontName"])
		
		self.writeNUByte(text["rgbaCol"][0])
		self.writeNUByte(text["rgbaCol"][1])
		self.writeNUByte(text["rgbaCol"][2])
		self.writeNUByte(text["rgbaCol"][3])
		
		self.writeBool(text["unknownBool1"])
		self.writeBool(text["unknownBool2"])
		self.writeBool(text["unknownBool3"])
		self.writeBool(text["unknownBool4"])
		
		self.writeByte(text["unknownByte1"])
		self.writeByte(text["unknownByte2"])
		
		self.writeShort(text["unknownShort1"])
		self.writeShort(text["unknownShort2"])
		self.writeShort(text["unknownShort3"])
		self.writeShort(text["unknownShort4"])
		
		self.writeBool(text["unknownBool5"])
		self.writeString(text["text"])
		
		if "extra" in text:
			self.tag = 15
			
			extra = text["extra"]
			
			self.writeBool(extra["unknownBool6"])
			
			if "rgbaCol" in extra:
				self.tag = 21
				
				self.writeNUByte(extra["rgbaCol"][0])
				self.writeNUByte(extra["rgbaCol"][1])
				self.writeNUByte(extra["rgbaCol"][2])
				self.writeNUByte(extra["rgbaCol"][3])
			
			if "unknownShort5" and "unknownShort6" in extra:
				self.tag = 33
				
				self.writeShort(extra["unknownShort5"])
				self.writeShort(extra["unknownShort6"])
				
				if "unknownShort7" and "unknownBool7" in extra:
					self.tag = 44
					
					self.writeShort(extra["unknownShort7"])
					self.writeBool(extra["unknownBool7"])
		
		self.length = len(self.stream.buffer)
