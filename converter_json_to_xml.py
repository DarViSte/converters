"""
21.09.2021

Daria Stepanova

Converting json file to xml

input: 
		json file,  image source directory, train image dir, train annotations dir, validation image dir, validation annotations dir
output: 
		anotations directory
		image directory
		
"""
import sys
import json
import xml.etree.cElementTree as ET
import shutil

if len(sys.argv) != 7:
	print("To run file, please use follow format:")
	print("python3 convert_json_to_xml.py json_file source_dir train_annotation_dir train_image_dir validationn_annotation_dir validation_image_dir")
	exit(-1) # or deal with this case in another way

json_file = sys.argv[1]
source_dir = sys.argv[2] 
train_annotation_dir = sys.argv[3]
train_image_dir = sys.argv[4]
validation_annotation_dir = sys.argv[5]
validation_image_dir = sys.argv[6]
    
with open('small_snow_road.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)
print ("All images = "+str(len(obj)))
train_num = int(len(obj)*0.75)
print ("Training images = "+str(train_num))
validation_num = int(len(obj)*0.25)
print ("Validation images = "+str(validation_num))


i = 0
for obj_str in obj:
	
	file_path = str(obj_str['image_path']).split('/')
	xml_name = file_path[1]
	xml_name = xml_name[:-5]
	xml_file_path = xml_name+".xml"
	
	root = ET.Element("annotation")
	
	ET.SubElement(root, "folder").text="snow_road"
	
	ET.SubElement(root, "filename").text = str(file_path[1])
	ET.SubElement(root, "path").text = source_dir+str(file_path[1])
	
	source = ET.SubElement(root, "source")
	ET.SubElement(source, "database").text = "Unknown"
    
	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = str(obj_str['width'])
	ET.SubElement(size, "height").text = str(obj_str['height'])
	ET.SubElement(size, "depth").text = "3"
    
	ET.SubElement(root, "segmented").text="0"
    
	for rect in obj_str['rects']:
		if ((str(rect['label']).find('snow_on_road') != -1) or (str(rect['label']).find('snow_on_sideroad') != -1)):
			objects = ET.SubElement(root, "object")
			ET.SubElement(objects, "name").text= str(rect['label'])
			ET.SubElement(objects, "pose").text = "Unspecified"
			ET.SubElement(objects, "truncated").text = "0"
			ET.SubElement(objects, "difficult").text = "0"
			
			bndbox = ET.SubElement(objects, "bndbox")
			ET.SubElement(bndbox, "xmin").text= str(rect['x1'])
			ET.SubElement(bndbox, "ymin").text= str(rect['y1'])
			ET.SubElement(bndbox, "xmax").text= str(rect['x2'])
			ET.SubElement(bndbox, "ymax").text= str(rect['y2'])	
	
	
	tree = ET.ElementTree(root)
	
	if (i<train_num):
		annotation_path = train_annotation_dir+xml_file_path
		image_path = train_image_dir+file_path[1]
		
	else:
		annotation_path = validation_annotation_dir+xml_file_path
		image_path = validation_image_dir+file_path[1]
	
	with open(annotation_path, "wb") as f:
		tree.write(f)
	shutil.copyfile(source_dir+str(file_path[1]), image_path)

	i=i+1
 
