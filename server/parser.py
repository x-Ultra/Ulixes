def parse_request(http_request): 

	try:
		params = http_request.split("\n")[0].split(" ")[1][2:].split("&")
	except:
		return "Invalid request"

	dict_params = {}
	for i in params:
		splitted = i.split("=")
		dict_params[splitted[0]] = splitted[1]

	return dict_params




