# coding:utf-8
def in_list(el, list):
	flag = False

	for i in list:
		if i == el:
			flag = True
			break

	return flag
