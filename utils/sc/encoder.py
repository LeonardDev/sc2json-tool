from ..writer import Writer

from .block import ScBlock

from .blocks.modifier import Modifier
from .blocks.texture import TextureSWF
from .blocks.shape import Shape
from .blocks.text import TextField
from .blocks.matrix import Matrix
from .blocks.color import ColorTransform
from .blocks.movieclip import MovieClip



class SwfWriter(Writer):
	def __init__(self, data: dict):
		super().__init__("<")
		self.data = data
		
		self.options = data["options"]
		self.modifiers = data["modifiers"]
		self.textures = data["textures"]
		self.shapes = data["shapes"]
		self.texts = data["textFields"]
		self.movieclips = data["movieClips"]
		self.matrices = []
		self.color_transforms = []
	
	def encode(self):
		self.make_transforms()
		
		# Sc Header
		self.writeUShort(len(self.shapes))
		self.writeUShort(len(self.movieclips))
		self.writeUShort(len(self.textures))
		self.writeUShort(len(self.texts))
		self.writeUShort(len(self.matrices))
		self.writeUShort(len(self.color_transforms))
		
		# Padding
		self.writeUByte(0)
		self.writeUInt32(0)
		
		# Export Names
		self.encode_exports()
		
		# Sc Blocks
		self.encode_tags()
	
	def encode_exports(self):
		export_ids = []
		export_names = []
		for clip in self.movieclips:
			if "names" in clip:
				for name in clip["names"]:
					export_ids.append(clip["id"])
					export_names.append(name)
		
		assert len(export_ids) == len(export_names)
		self.writeUShort(len(export_ids))
		for id in export_ids:
			self.writeUShort(id)
		
		for name in export_names:
			self.writeString(name)
	
	def encode_tags(self):
		# Options
		if self.options["hasHighresFile"]:
			self.writeUByte(23)
			self.writeUInt32(0)
		
		if self.options["hasExternalTexFile"]:
			self.writeUByte(26)
			self.writeUInt32(0)
		
		if self.options["hasLowresFile"]:
			self.writeUByte(30)
			self.writeUInt32(0)
		
		# Movie Clip Modificators
		
		for modifier in self.modifiers:
			modifier_data = Modifier(modifier["modifierType"])
			modifier_data.encode(modifier)
			
			self.write_block(modifier_data)
		
		# SWF Textures
		for texture in self.textures:
			texture_data = TextureSWF(1)
			texture_data.encode(texture)
			
			self.write_block(texture_data)
		
		# Shapes
		for shape in self.shapes:
			shape_data = Shape(18, self.textures)
			shape_data.encode(shape)
			
			self.write_block(shape_data)
		
		# Text Fields
		for text in self.texts:
			text_data = TextField(7)
			text_data.encode(text)
			
			self.write_block(text_data)
		
		# Transformation Matrices
		for matrix in self.matrices:
			matrix_data = Matrix(8)
			matrix_data.encode(matrix)
			
			self.write_block(matrix_data)
		
		# Color Transforms
		for color in self.color_transforms:
			color_data = ColorTransform(9)
			color_data.encode(color)
			
			self.write_block(color_data)
		
		# Movie Clips
		for clip in self.movieclips:
			movieclip = MovieClip(12)
			movieclip.encode(clip)
			
			self.write_block(movieclip)
		
		# End Tag
		self.writeUByte(0)
		self.writeUInt32(0)
	
	def make_transforms(self):
		for clip in self.movieclips:
			clip["transforms"] = []
			for frame in clip["data"]["frames"]:
				frame["count"] = len(frame["transforms"])
				for transform in frame["transforms"]:
					clip["transforms"].append(transform)
			
			for transform in clip["transforms"]:
				if "matrix" in transform:
					if transform["matrix"] not in self.matrices:
						self.matrices.append(transform["matrix"])
					transform["matrix"] = self.matrices.index(transform["matrix"])
				else:
					transform["matrix"] = 65535
				
				if "color" in transform:
					if transform["color"] not in self.color_transforms:
						self.color_transforms.append(transform["color"])
					transform["color"] = self.color_transforms.index(transform["color"])
				else:
					transform["color"] = 65535
	
	def write_block(self, block: ScBlock):
		tag = int(block.tag).to_bytes(1, "little")
		length = int(block.length).to_bytes(4, "little", signed=False)
		data = block.stream.buffer
		
		result = tag + length + data
		self.stream.write(result)
