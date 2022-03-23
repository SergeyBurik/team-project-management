# coding:utf-8
import json
from websocket import create_connection
from lamp import settings


def in_list(el, list):
	flag = False

	for i in list:
		if i == el:
			flag = True
			break

	return flag


def websocket_send(req):
	# adding new teammate group chat
	ws = create_connection(settings.MESSENGER_URL)
	# send request
	ws.send(
		json.dumps(
			req
		)
	)

	# get response
	result = json.loads(ws.recv())
	if result['code'] == 500:
		raise Exception(result.message)

	ws.close()
	return result
