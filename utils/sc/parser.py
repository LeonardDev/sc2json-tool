from ..reader import Reader

from .blocks.modifier import Modifier
from .blocks.texture import TextureSWF
from .blocks.shape import Shape
from .blocks.text import TextField
from .blocks.matrix import Matrix
from .blocks.color import ColorTransform
from .blocks.movieclip import MovieClip



class SwfParser(Reader):
	def __init__(self, data: bytes):
		super().__init__(data)
		self.data = data
		
		self.exports = []
		
		self.has_external_texture = False
		self.has_lowres_texture = False
		self.has_highres_texture = False
		
		self.modifiers = []
		self.textures = []
		self.shapes = []
		self.texts = []
		self.matrices = []
		self.color_transforms = []
		self.movieclips = []
	
	def parse(self):
		# Sc Header
		for x in range(6):
			self.readUShort()
		
		# Padding
		self.readUByte()
		self.readUInt32()
		
		# Export Names
		exports_count = self.readUShort()
		for x in range(exports_count):
			self.exports.append([self.readUShort()])
		
		for x in range(exports_count):
			self.exports[x].append(self.readString())
		
		# Sc Blocks
		while not self.stream.eof():
			tag = self.readUByte()
			length = self.readUInt32()
			data = self.stream.read(length)
			
			if tag == 0:
				break
			
			elif tag == 23:
				self.has_lowres_texture = True
			
			elif tag == 26:
				self.has_external_texture = True
			
			elif tag == 30:
				self.has_highres_texture = True
			
			elif tag in [37, 38, 39, 40]: # Movie Clip Modificators
				modifier = Modifier(tag)
				
				self.modifiers.append(modifier.parse(data))
			
			elif tag in [1, 16, 24, 27, 28, 29, 34]: # SWF Texture
				texture = TextureSWF(tag)
				
				self.textures.append(texture.parse(data))
			
			elif tag in [2, 18]: # Shape
				shape = Shape(tag, self.textures)
				
				self.shapes.append(shape.parse(data))
			
			elif tag in [7, 15, 20, 21, 25, 33, 44]: # Text Field
				text = TextField(tag)
				
				self.texts.append(text.parse(data))
			
			elif tag in [8]: # Transformation Matrix
				matrix = Matrix(tag)
				
				self.matrices.append(matrix.parse(data))
			
			elif tag in [9]: # Color Transform
				color = ColorTransform(tag)
				
				self.color_transforms.append(color.parse(data))
			
			elif tag in [3, 12, 14, 35]: # Movie Clip
				clip = MovieClip(tag)
				
				self.movieclips.append(clip.parse(data))
			
			else:
				print("SupercellSWF::Unknown tag; {} {}".format(tag, length))
		
		print()
		
		# Some shit
		self.parse_exports()
		self.make_frames()
		self.make_transforms()
	
	def parse_exports(self):
		for clip in self.movieclips:
			for export in self.exports:
				if clip["id"] == export[0]:
					if "names" not in clip:
						clip["names"] = []
					clip["names"].append(export[1])
	
	def make_frames(self):
		for clip in self.movieclips:
			offset = 0
			new_frames = []
			
			for frame in clip["data"]["frames"]:
				new_frame = {}
				
				new_frame["name"] = frame["name"]
				new_frame["transforms"] = []
				for i in range(frame["count"]):
					new_frame["transforms"].append(clip["transforms"][offset + i])
				
				offset += frame["count"]
				new_frames.append(new_frame)
			
			clip["data"]["frames"] = new_frames
			del clip["transforms"]
	
	def make_transforms(self):
		for clip in self.movieclips:
			for frame in clip["data"]["frames"]:
				for transform in frame["transforms"]:
					if transform["matrix"] != 65535:
						transform["matrix"] = self.matrices[transform["matrix"]]
					else:
						del transform["matrix"]
						
					if transform["color"] != 65535:
						transform["color"] = self.color_transforms[transform["color"]]
					else:
						del transform["color"]
	
	def parsed_as_dict(self):
		return {
			"options": {
				"hasExternalTexFile": self.has_external_texture,
				"hasHighresFile": self.has_highres_texture,
				"hasLowresFile": self.has_lowres_texture
			},
			"modifiers": self.modifiers,
			"textures": self.textures,
			"shapes": self.shapes,
			"textFields": self.texts,
			"movieClips": self.movieclips
		}
