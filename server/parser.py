def parse_http_request(http_request): 

	#@ http_reqeust: string containing a get/post request from the http protocol
	#@ return:  a dict containing the url parameters of the request and the http version

	#split the url
	try:
		first_line = http_request.split("\n")[0].split(" ")
		params = first_line[1][2:].split("&")
		version = first_line[2].strip()
	except:
		return "Invalid request"

	if len(params) < 4:
		return "Invalid request"	
		
	#load result in dict
	dict_params = {}
	for i in params:
		splitted = i.split("=")
		dict_params[splitted[0]] = splitted[1]

	dict_params["version"] = version
	return dict_params

def make_http_response(return_code, http_version =None, json=None):

	#@ return code: integer, the return code of the response from the http protocol 
	#@ http_version: string, the http version to use for the response
	#@ json: in case of ret_code=200, the json string to add in the body of the response

	#@ return: a string containing the http response

	if (return_code == 400):
		return "400 Bad Request\r\n"
	elif (return_code == 200):
		return http_version + " 200 OK\r\n" + "Content-Type: application/json\r\n\r\n" + json
	else:
		print("Not supported")
		return None



