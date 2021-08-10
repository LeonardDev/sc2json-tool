from ..block import ScBlock

from .subs.frame import MovieFrame
from .subs.grid import MovieGrid
from .subs.value import MovieValue



class MovieClip(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		clip = {}
		
		clip["id"] = self.readUShort()
		
		clip["frameRate"] = self.readUByte()
		self.readUShort() # frames count
		
		clip["binds"] = []
		
		clip["transforms"] = []
		if self.tag != 14:
			for x in range(self.readUInt32()):
				clip["transforms"].append({
					"bindIndex": self.readUShort(),
					"matrix": self.readUShort(),
					"color": self.readUShort()
				})
		
		binds_count = self.readUShort()
		
		for x in range(binds_count):
			clip["binds"].append({
				"bindId": self.readUShort(),
				"blend": 0,
				"name": None
			})
		
		if self.tag in [12, 35]:
			for x in range(binds_count):
				clip["binds"][x]["blend"] = self.readByte()
		
		for x in range(binds_count):
			clip["binds"][x]["name"] = self.readString()
		
		clip["data"] = self.parse_frames()
		
		return clip
	
	def parse_frames(self):
		frames = {}
		
		frames["frames"] = []
		frames["grids"] = []
		frames["values"] = []
		
		while True:
			tag = self.readUByte()
			length = self.readUInt32()
			data = self.stream.read(length)
			
			if tag == 0:
				break
			elif tag == 11:
				frame = MovieFrame(tag)
				frames["frames"].append(frame.parse(data))
			elif tag == 31:
				grid = MovieGrid(tag)
				frames["grids"].append(grid.parse(data))
			elif tag == 41:
				value = MovieValue(tag)
				frames["values"].append(value.parse(data))
			else:
				print("SupercellSWF::Unknown tag in MovieClipFrames; {} {}".format(tag, length))
		
		return frames
	
	def encode(self, clip: dict):
		super().encode()
		
		self.writeUShort(clip["id"])
		self.writeUByte(clip["frameRate"])
		self.writeUShort(len(clip["data"]["frames"]))
		
		if self.tag != 14:
			self.writeUInt32(len(clip["transforms"]))
			for transform in clip["transforms"]:
				self.writeUShort(transform["bindIndex"])
				self.writeUShort(transform["matrix"])
				self.writeUShort(transform["color"])
		
		self.writeUShort(len(clip["binds"]))
		for bind in clip["binds"]:
			self.writeUShort(bind["bindId"])
		
		if self.tag in [12, 35]:
			for bind in clip["binds"]:
				self.writeByte(bind["blend"])
		
		for bind in clip["binds"]:
			self.writeString(bind["name"])
		
		self.encode_frames(clip["data"])
		
		self.length = len(self.stream.buffer)
	
	def encode_frames(self, data: dict):
		for value in data["values"]:
			value_data = MovieValue(41)
			value_data.encode(value)
			
			self.writeUByte(value_data.tag)
			self.writeUInt32(value_data.length)
			self.stream.write(value_data.stream.buffer)
		
		for frame in data["frames"]:
			frame_data = MovieFrame(11)
			frame_data.encode(frame)
			
			self.writeUByte(frame_data.tag)
			self.writeUInt32(frame_data.length)
			self.stream.write(frame_data.stream.buffer)
		
		for grid in data["grids"]:
			grid_data = MovieGrid(31)
			grid_data.encode(grid)
			
			self.writeUByte(grid_data.tag)
			self.writeUInt32(grid_data.length)
			self.stream.write(grid_data.stream.buffer)
		
		self.writeUByte(0)
		self.writeUInt32(0)
