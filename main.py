import os
import sys
import json

from sc_compression.signatures import Signatures
from sc_compression.decompressor import Decompressor
from sc_compression.compressor import Compressor

from utils.sc.parser import SwfParser
from utils.sc.encoder import SwfWriter



decompressor = Decompressor()
compressor = Compressor()


def to_json(path):
	file = open(path, 'rb')
	file_data = decompressor.decompress(file.read())
	file.close()
	
	sc_parser = SwfParser(file_data)
	sc_parser.parse()
	
	parsed = sc_parser.parsed_as_dict()
	
	save_path = os.path.splitext(path)[0] + ".json"
	
	json.dump(parsed, open(save_path, 'w'), indent=4)
	
	print("Saved as {}!".format(save_path))


def to_sc(path):
	file = open(path, 'r')
	file_data = json.loads(file.read())
	file.close()
	
	sc_writer = SwfWriter(file_data)
	sc_writer.encode()
	
	result = sc_writer.stream.buffer
	result = compressor.compress(result, Signatures.SC, 1)
	
	save_path = os.path.splitext(path)[0] + "_patched.sc"
	
	file = open(save_path, 'wb')
	file.write(result)
	file.close()
	
	print("Saved as {}!".format(save_path))


def decompress_sc(path):
	file = open(path, 'rb')
	file_data = decompressor.decompress(file.read())
	file.close()
	
	save_path = os.path.splitext(path)[0] + "_dec.sc"
	
	file = open(save_path, 'wb')
	file.write(file_data)
	file.close()
	
	print("Decompressed! Saved as {}!".format(save_path))


def compress_sc(path):
	file = open(path, 'rb')
	file_data = compressor.compress(file.read(), Signatures.SC, 1)
	file.close()
	
	save_path = os.path.splitext(path)[0] + "_cmp.sc"
	
	file = open(save_path, 'wb')
	file.write(file_data)
	file.close()
	
	print("Выполнено! Сохранено как {}!".format(save_path))


if __name__ == "__main__":
	args = sys.argv
	
	if len(args) < 2:
		print("Input the name of operation and file path")
		print("Example: python main.py <sc2json or json2sc> <file path>")
		sys.exit()
	
	op = args[1]
	path = args[2]
	
	if op in ["sc2json", "SC2JSON"]:
		to_json(path)
	
	elif op in ["json2sc", "JSON2SC"]:
		to_sc(path)
	
	elif op in ["d"]:
		decompress_sc(path)
	
	elif op in ["c"]:
		compress_sc(path)
	
	else:
		print("Unknown operation name!")
		print("Use 'sc2json' or 'json2sc'!")
		sys.exit()
