# getting raw html_template for input
def get_html_template():
	with open("template.html") as f:
		template = f.read()
	return template

# data: string including list of dictionaries for every cube, including links to images
# x: string including name of x variable
# y: string including name of y variable
# z: string including name of z variable
def update_html_template(data,x,y,z):
	template = get_html_template()
	template = template.replace("INSERT_DATA_HERE",data)
	template = template.replace("INSERT_X_HERE",x)
	template = template.replace("INSERT_Y_HERE",y)
	template = template.replace("INSERT_Z_HERE",z)
	return template
