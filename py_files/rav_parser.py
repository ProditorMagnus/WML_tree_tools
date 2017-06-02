#!/usr/bin/env python3
# encoding: utf-8

from os.path import join
import wmlparser3

mode = 0b10000000 # show debug | show real | show extra log | dryrun, do not parse | something for future if needed
def debug():
	return mode & 0b10000000

def prod():
	return mode & 0b01000000

def extra():
	return mode & 0b00100000

def dryrun():
	return mode & 0b00010000

main = wmlparser3.Parser()

if not dryrun(): 
	root_node = main.parse_file(join("..","preprocessed_addon","_main.cfg"))

# debug = mode & 0b10000000, debug and print()

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

def query_matches(node, path, query):
	# tag_path = path # for dry testing
	tag_path = [n.get_name() for n in path] # not for dry testing
	# TODO add support for *
	query_path = query[0]
	if debug() and "unit_type" not in tag_path:
		# only for debug
		return False
	if debug() and len(tag_path) != len(query_path):
		return False
	query_pos = 0
	tag_pos = 0
	found_pos = 0
	i = 0
	while found_pos < len(query_path) and i < 20 and tag_pos < len(tag_path) and query_pos < len(query_path):
		i+=1
		if tag_path[tag_pos] == query_path[query_pos]:
			if extra(): print("found", tag_pos, query_pos, tag_path, query_path)
			query_pos+=1
			tag_pos+=1
			found_pos+=1
		else:
			if extra(): 
				print("* not supported", tag_path, query_path)
				input()
			return False
			# TODO handle *
	if found_pos < len(query_path):
		# so loop ended too quickly
		if debug(): print("loop ended at",found_pos, "expected",len(query_path))
		return False
	# so it found suitable tag place
	# check attribute then
	attr_query = query[1]
	if attr_query is not None:
		if node.get_name() != attr_query[0]:
			return False
		attr_value = node.get_text()
		attr_wanted = attr_query[1]
		if attr_value is not None and attr_wanted=="*":
			return True
		else:
			if extra(): 
				print("attr check not finished")
				print("got",attr_value, "wanted", attr_wanted)
				input()
			if attr_value != attr_wanted:
				# print("got",attr_value, "wanted", attr_wanted)
				return False
	
	return True
	
def find_from_wml(node, path, query):
	if len(path) > len(query[0]) and not "*" in query[0]:
		# only looked trees of limited depth
		return
	if isinstance(node, wmlparser3.TagNode):
		for child in node.get_all():
			if isinstance(child, wmlparser3.TagNode):
				find_from_wml(child, path+[child], query)
			else:
				find_from_wml(child, path, query)
	elif isinstance(node, wmlparser3.AttributeNode):
		# check if something is being searched from this path
		if query_matches(node, path, query):
			printable_path = [n.get_name() for n in path]
			printable_ids = [n.get_text_val("id") for n in path]
			if debug(): print("found match at",printable_path, printable_ids)
		# else:
			# if extra(): print("no match at",printable_path)

def parse_wml_query(query):
	path_wanted = []
	attr_wanted = None
	query = query.split(">")
	for item in query:
		if item == "":
			path_wanted.append("*")
		elif len(item)>2 and item[0]=="[" and item[-1]=="]":
			path_wanted.append(item[1:-1])
		else:
			# this should be attribute query then
			# TODO parse attr filter
			if "==" in item:
				item = item.split("==",1)
				attr_wanted = (item[0], item[1])
			else:
				attr_wanted = (item, "*")
	return path_wanted, attr_wanted


# explore_wml(root_node, [])
# query made of tag path, ending with single attribute request
query = parse_wml_query("[units]>[unit_type]>[attack]>damage==25")
print(query)
# print(query_matches(None, ["unit_type", "attack", "specials"], query))

find_from_wml(root_node, [], query)