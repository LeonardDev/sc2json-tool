from ..reader import Reader
from ..writer import Writer



class ScBlock(Reader, Writer):
	def __init__(self, tag: int = 0):
		self.tag = tag
		
		self.length = 0
	
	def parse(self, data: bytes):
		Reader.__init__(self, data, "<")
	
	def encode(self):
		Writer.__init__(self, "<")
		
		self.length = len(self.stream.buffer)
