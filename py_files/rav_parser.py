#!/usr/bin/env python3
# encoding: utf-8

import wmlparser3

mode = 0b01000000 # show debug | show real | show extra log | something for future if needed

main = wmlparser3.Parser()

root_node = main.parse_file(r"C:\Users\Ravana\Desktop\general\wesnoth-related\dev1.13.8\parse_tree\ageless_preprocessed\_main.cfg")

def debug():
	return mode & 0b10000000

def prod():
	return mode & 0b01000000

def extra():
	return mode & 0b00100000

def find_inner_from_path(path, tag):
	for i in range(len(path)-1, -1, -1):
		node = path[i]
		if node.get_name() == tag:
			return node

def explore_wml(node, path):
	printable_path = [n.get_name() for n in path]
	if isinstance(node, wmlparser3.TagNode):
		try:
			name = node.get_name()
		except:
			if extra(): print("getting name failed for",printable_path)
			node.name = "no_name_defined"
			name = "no_name_defined"
					
		if name == "event":
			if node.get_text_val("id") is None:
				if "unit_type" in printable_path:
					if debug(): print(find_inner_from_path(path, "unit_type").get_text_val("id"), "has event without id", node.get_text_val("name"), printable_path)
					if prod(): print("MISSING_ID:",find_inner_from_path(path, "unit_type").get_text_val("id"),":",node.get_text_val("name"))
				else:
					if extra(): print("found event without id at",printable_path, node.get_text_val("name"), node.debug()[:100])
				
				# input()
		for child in node.get_all():
			explore_wml(child, path+[child])

explore_wml(root_node, [])