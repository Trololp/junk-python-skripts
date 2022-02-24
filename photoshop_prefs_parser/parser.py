from struct import unpack
from datetime import datetime
import sys



def bytes_to_str(bytes_str):
	tmp = ""
	for b in bytes_str:
		tmp += chr(b)
	return tmp

def bytes_to_wstr(bytes_str, shesh):
	tmp = ""
	
	for i in range(len(bytes_str) - 2):
		if (i + shesh) % 2:
			tmp += chr(bytes_str[i])
		
	
	return tmp		

def parse_descr(f):
	descr_size = unpack('>I', f.read(4))[0]
	if descr_size == 0:
		descr_size = 4
	descr_str_b = f.read(descr_size)
	return unpack('%ds' % descr_size, descr_str_b)[0].decode("utf-8")

def parse_bool(f):
	data = f.read(1)
	return "True" if data == b'\x01' else "False"
	
def parse_long(f):
	data = f.read(4)
	return ("%d" % unpack(">I", data)[0])

def parse_TEXT(f):
	TEXT_size = unpack('>I', f.read(4))[0]
	TEXT_string = bytes_to_wstr(f.read(TEXT_size * 2), 0) #f.read(TEXT_size * 2).decode('UTF-16-LE')#
	return '"' + TEXT_string + '"'

def parse_tdta(f):
	tdta_len = unpack('>I', f.read(4))[0]
	f.seek(tdta_len, 1) #some blob data
	return "tdta"

def parse_comp(f):
	(unk1, unk2) = unpack('>II', f.read(8))
	return ("comp %d %d" % (unk1, unk2))

def parse_Pth(f):
	pth_size  = unpack('>I', f.read(4))[0]
	file_pos = f.seek(0, 1)
	data_ident = f.read(4)
	
	
	
	if(data_ident != b'txtu'):
		
		if(data_ident == b'\x00\x00\x00\x00'):
			offset = unpack('>H', f.read(2))[0]
			f.seek(offset - 6, 1)
			data_ident2 = f.read(5)
			if(data_ident2 != b' LRUD'):
				print("error unknown Pth %x" % f.seek(0, 1))
				f.seek(file_pos - 4 + pth_size, 0)
				return "Pth error"
			data_size = unpack('>I', f.read(4))[0]
			f.seek(3, 1)
			return "url:\"" + unpack('%ds' % data_size, f.read(data_size))[0].decode("utf-8") + '"'
			
		print("error unknown Pth %x" % f.seek(0, 1))
		f.seek(file_pos - 4 + pth_size, 0)
		return "Pth error"
		
	unk2 = unpack('I', f.read(4))[0]
	txt_len = unpack('I', f.read(4))[0]
	txt_string = bytes_to_wstr(f.read(txt_len * 2), 1) # f.read(txt_len * 2).decode('UTF-16-BE')# 
	return '"' + txt_string + '"'

def parse_enum(f):
	enum1 = parse_descr(f)
	enum2 = parse_descr(f)
	return ("{0: %s 1: %s}" % (enum1, enum2))

def parse_doub(f):
	double_val = unpack('d', f.read(8))[0]
	return "%f" % double_val

def parse_UntF(f):
	(a, b, c) = unpack('III', f.read(12))
	return "UntF {%x %x %x}" % (a, b, c)

def parse_type(f):
	type = f.read(4) 
	
	f_table = {
		b'bool' : lambda f: parse_bool(f),
		b'long' : lambda f: parse_long(f),
		b'TEXT' : lambda f: parse_TEXT(f),
		b'tdta' : lambda f: parse_tdta(f),
		b'comp' : lambda f: parse_comp(f),
		b'Pth ' : lambda f: parse_Pth(f) , 
		b'VlLs' : lambda f: parse_VlLs(f),
		b'Objc' : lambda f: parse_Objc(f),
		b'enum' : lambda f: parse_enum(f),
		b'doub' : lambda f: parse_doub(f),
		b'UntF' : lambda f: parse_UntF(f)
	}
	
	if type not in f_table:
		print("new type: ", type, f.seek(0, 1))
		sys.exit(0)
	
	return f_table[type](f)

def is_type_str(type):
	
	tbl = [b'TEXT', b'Pth ']
	
	if type in tbl:
		return True
	
	return False
	

g_identation_lvl = 0

def parse_VlLs(f):
	global g_identation_lvl
	amount = unpack('>I', f.read(4))[0]
	
	VlLs_desc = "VlLs { \n"
	
	g_identation_lvl += 1
	
	for i in range(amount):
		VlLs_desc += (g_identation_lvl * "\t" + "%d: " % i + parse_type(f) + '\n')
	
	g_identation_lvl -= 1
	
	VlLs_desc += g_identation_lvl * "\t" + "} \n"
	
	return VlLs_desc

def get_list_VlLs_type(f):
	vals = []
	
	type = f.read(4) 
	
	if type != b'VlLs':
		print("type != VlLs \n")
		return vals
	
	amount = unpack('>I', f.read(4))[0]
	
	for i in range(amount):
		vals.append(parse_type(f))

	return vals



def parse_Objc(f):
	global g_identation_lvl
	
	utf16_descr_len = unpack(">I", f.read(4))[0]
	
	f.seek(utf16_descr_len * 2, 1)
	
	descr_len = unpack('>I', f.read(4))[0]
	if descr_len == 0:
		descr_len = 4
	
	name = unpack('%ds' % descr_len, f.read(descr_len))[0].decode("utf-8")
	amt = unpack('>I', f.read(4))[0]
	
	obj_c_desc = "Objc %s { \n" % (name)
	
	g_identation_lvl += 1

	for i in range(amt):
		desc_str = parse_descr(f)
		data = parse_type(f)

		obj_c_desc += (g_identation_lvl * "\t" + desc_str + ' : ' + data + '\n')
	
	g_identation_lvl -= 1
	
	obj_c_desc += g_identation_lvl * "\t" + "}\n"
	
	return obj_c_desc
	

def parse_first_objc_get_field_loc(f, field):

	f.seek(0xA, 0) # return to start
	utf16_descr_len = unpack(">I", f.read(4))[0]
	f.seek(utf16_descr_len * 2, 1)
	
	descr_len = unpack('>I', f.read(4))[0]
	if descr_len == 0:
		descr_len = 4
	
	f.read(descr_len)
	#name = unpack('%ds' % descr_len, )[0].decode("utf-8")
	amt = unpack('>I', f.read(4))[0]

	
	for i in range(amt):
		desc_str = parse_descr(f)
		
		if(desc_str == field):
			return f.seek(0, 1)
		
		data = parse_type(f)

		#obj_c_desc += (g_identation_lvl * "\t" + desc_str + ' : ' + data + '\n')
	
	
	return -1

def just_print_info(f):
	print(parse_Objc(f))
	return



def just_print_last_works_info(f):

	MRUL_loc = parse_first_objc_get_field_loc(f, "MRUL")
	if MRUL_loc == -1:
		print("MRUL not found")
		return
	
	f.seek(MRUL_loc, 0)
	
	works_count  = int(parse_type(f))
	
	print("Amount of works: %d\n" % works_count)
	
	MRUA_loc = parse_first_objc_get_field_loc(f, "MRUA")
	
	if MRUA_loc == -1:
		print("MRUA not found")
		return
	
	f.seek(MRUA_loc, 0)
	
	Works_names = get_list_VlLs_type(f)
	
	MRUD_loc = parse_first_objc_get_field_loc(f, "MRUD")
	
	if MRUD_loc == -1:
		print("MRUD not found")
		return
	
	f.seek(MRUD_loc, 0)
	
	Works_dates_str = get_list_VlLs_type(f)
	
	for i in range(works_count):
		ts = int(Works_dates_str[i])
		time_str = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print("%d: %s\nEdited UTC: %s \n" % (i, Works_names[i], time_str))
	
	return

"""
def modify_bytestr(bs, start_p, end_p, new_data):
	return bs[:start_p] + new_data + bs[end_p:]

def f_remove_contents_VlLs(bs, start_p, end_p, id)
	
	type = bs[start_p:start_p + 4] 
	
	if type != b'VlLs':
		print("type != VlLs \n")
		return vals
	
	amount = unpack('>I', bs[start_p + 4:start_p + 8])[0]
	
	for i in range(amount):
		vals.append(parse_type(f))

def remove_work(f):

	MRUL_loc = parse_first_objc_get_field_loc(f, "MRUL")
	if MRUL_loc == -1:
		print("MRUL not found")
		return
	
	f.seek(MRUL_loc, 0)
	
	works_count  = int(parse_type(f))

	MRUA_loc = parse_first_objc_get_field_loc(f, "MRUA")
	
	if MRUA_loc == -1:
		print("MRUA not found")
		return
	
	f.seek(MRUA_loc, 0)
	
	Works_names = get_list_VlLs_type(f)

	for i in range(len(Works_names)):
		print(i, Works_names[i])

	print("Chose work to remove\n")
	
	id_str = input("id to remove:")
	
	if !id_str.isnumeric():
		print("require numeric input")
		return
	
	if int(id_str) < 0:
		print("require numeric input >0")
		return
	
	id = int(id_str)
	
	size = f.seek(0, 2)
	f.seek(0, 0)
	file_contents = f.read(size)
	
	
	
	return
"""


def Usage_print():
	print("Usage: [option] [preference_file]")
	print("info: Dump preference_file content to stdout")
	print("works: display last works")
	#print("remove_work: remove specific last work from preference_file")
	return



def main(argv):
	
	if len(argv) < 2:
		Usage_print()
		sys.exit(0)
	
	option_handle_functions = {
	"info" : lambda a: just_print_info(a),
	"works" : lambda a: just_print_last_works_info(a)
	#"remove_work" : lambda a: remove_work(a)
	}
	
	if argv[0] not in option_handle_functions:
		Usage_print()
		sys.exit(0)
	
	
	
	f = open(argv[1], 'rb')
	
	hdr = f.read(0xA)

	if (hdr[0:4] != b'8BPF'):
		print("wrong file")
		sys.exit(0)
	
	option_handle_functions[argv[0]](f)
	
	

if __name__ == "__main__":
   main(sys.argv[1:])
