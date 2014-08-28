#coding=utf-8
from subtitle import *

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	print ('Welcome to YYETS subtitle search script')
	# Check if .yysub in ~/ directory
	sub = Subtitle()
	sub.getJsonData()

	task = YYETS()
	utl = utility()

	searchKey = utl.showAndInput(0)
	while searchKey != 'q':
		page = task.fetchSubtitle(searchKey)    
		task.showAndDownload(page)
		searchKey = utl.showAndInput(0)
	print ('bye!')	


if __name__ == '__main__':
	main()