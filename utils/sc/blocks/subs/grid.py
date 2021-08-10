from ...block import ScBlock



class MovieGrid(ScBlock):
	def __init__(self, tag: int):
		super().__init__(tag)
	
	def parse(self, data: bytes):
		super().parse(data)
		
		grid = {}
		
		grid["x"] = self.readInt32() / 20
		grid["y"] = self.readInt32() / 20
		
		grid["width"] = self.readInt32() / 20 + grid["x"]
		grid["height"] = self.readInt32() / 20 + grid["y"]
		
		return grid
	
	def encode(self, grid: dict):
		super().encode()
		
		self.writeInt32(round(grid["x"] * 20))
		self.writeInt32(round(grid["y"] * 20))
		
		self.writeInt32(round((grid["width"] - grid["x"]) * 20))
		self.writeInt32(round((grid["height"] - grid["y"]) * 20))
		
		self.length = len(self.stream.buffer)
