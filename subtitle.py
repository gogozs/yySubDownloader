#coding=utf8

from lxml import etree
from urllib2 import Request, urlopen
from urllib import urlretrieve
import sys
import re
import subprocess
import os
import json

class Subtitle(object):
	YYETS = '【人人影视原创翻译】'
	cwd = os.getcwd()
	app = '' # Th unarchiver app path
	langPriority = [] # subtitle language priority list

	def __init__(self):
		self.id = 0
		self.downloadURL = ''
		self.edition = ''
		self.yyFlag = 0 # yyFlag = 1 -> show YYETS

	def showSub(self):
		print '【' + str(self.id) + '】' + self.edition + (self.yyFlag == 1 and Subtitle.YYETS or '') + '\n'

	def download(self):
		print('Downloading'+ '【'+str(self.id)+'】'+ self.edition + '…')
		saveURL = Subtitle.cwd + '/'+ self.edition + '.rar'
		urlretrieve(self.downloadURL,saveURL, reporthook=Subtitle.reporthook)
		# Create a child process, run shell commands
		child = subprocess.Popen([Subtitle.app,saveURL])
		child.wait()

		dirPath = Subtitle.cwd + '/' + self.edition + '/' # sub dir path
		subFiles = os.listdir(dirPath) # sub files


		priorityIndex = subIndex = 0
		while subIndex in range(0, len(subFiles)):
			# regular expression in langPriority[priorityIndex]

			try:
				res = Subtitle.langPriority[priorityIndex].encode('utf8').split('-')
				pattern = '.*'
				pattern = pattern.join(res).lower() # e.g. 简体.*英文.*srt
			except IndexError:
				print "Can't choose preferred subtitle (Out of LangPriority list)"
				break


			if re.search(pattern, subFiles[subIndex]):
				print subFiles[subIndex] + ' is moving to ' + Subtitle.cwd +'\n'
				proc = subprocess.Popen(['mv',dirPath+subFiles[subIndex],Subtitle.cwd])
				proc.wait()
				break
			else:
				if subIndex == len(subFiles) - 1 and priorityIndex < len(Subtitle.langPriority): # Prepare next while loop
					subIndex = 0 # Empty subIndex count
					priorityIndex += 1 # Next language priority
				else:
					subIndex += 1

		subprocess.Popen(['sudo','rm','-rf',dirPath,saveURL])


	def getJsonData(self):
		home = os.path.expanduser('~')

		try:
			json_file = open(home + '/.yysub', 'r')
			json_data = json.load(json_file)	
			Subtitle.app = json_data["app"]
			Subtitle.langPriority = json_data["langPriority"]
		except:
			print "!!! Please `cp yySubDownloader/.yysub ~/.yysub`"
			print "the .yyusb file is hidden, please use Terminal."
			exit(0)

	@staticmethod
	def reporthook(block_read,block_size,total_size):
		if not block_read:
			print(u"\U0001F3A5"+"  "),
		if total_size<0:
		#unknown size
			print "read %dB" %(block_read,block_read*block_size)
		else:
			if (block_read * block_size < total_size):
				sys.stdout.write('#')
				sys.stdout.flush()
			else:	
				print (' done!')

class YYETS(object):

	def fetchSubtitle(self, searchKey):
		reload(sys)
		sys.setdefaultencoding('utf8')

		# Encode the URL
		subUrl = ("http://www.yyets.com/search/index?keyword="+searchKey+"&type=subtitle").encode('utf8')

		# Request to the URL
		req = Request(subUrl)
		resp = urlopen(req)
		respHtml = resp.read()
		resp.close()

		# Handle the page
		page = etree.HTML(respHtml.decode("utf-8"))

		return page

	def showAndDownload(self, page):
		resultURLs =  page.xpath(u"//div[@class='all_search_li2']/a") # an URL list
		utl = utility()

		if len(resultURLs):
			subList = [] # List contains subtitle objects
			index = 2

			# Add subtitle info in subtitle objects
			for resultURL in resultURLs:
				sub = Subtitle() # an subtitle object

				# Add subtitle info
				ID = resultURL.attrib['href'].rsplit('/',1)[1] # e.g., href="http://www.yyets.com/subtitle/39432"	
				sub.downloadURL = "http://www.yyets.com/subtitle/index/download?id=" + ID
				sub.id = index-1
				sub.edition = page.xpath(u"/html/body/div[6]/div[4]/div/ul/li["+str(index)+"]/div[2]/p/text()")[1]	
				if len(page.xpath(u"/html/body/div[6]/div[4]/div/ul/li["+str(index)+"]/div[2]/div[1]/a/strong[2]/text()")):
					sub.yyFlag = 1

				subList.append(sub)
				index += 1

			# Show subtitles info
			for sub in subList:
				sub.showSub()

			# Choose the number to download
			number = utl.showAndInput(1) 
			while(number != 'q'):
				if (number.isdigit()): # Single selection, e.g., (1)
					if (int(number) > 0 and int(number) < len(subList) + 1):
						for sub in subList:
							if sub.id == int(number):
								sub.download()
						number = utl.showAndInput(1)
					else:
						number = utl.showAndInput(3)
				elif (number.find('-') == 1):# Range selection, e.g., (1-5)
					subRange = range(int(number.split('-')[0]), int(number.split('-')[1]) + 1)

					for sub in subList:
						if sub.id in subRange:
							sub.download()
					number = utl.showAndInput(1)
				elif (number.find(',') == 1): # Nonsequenced selection, e.g., (1,3,5)
					subRange = number.split(',')
					for i in range(0,len(subRange)):
						for sub in subList:
							if sub.id == int(subRange[i]):
								sub.download()
								break

					number = utl.showAndInput(1)
				else:
					number = utl.showAndInput(4)
		else:
			# No result
				number = utl.showAndInput(2) 
			
				


class utility(object):
	def showAndInput(self,mode):
		if mode == 0:
			print "Input video name to search or ('q' to quit)"
			input = raw_input('>>')
			return input
		elif mode == 1:
			print "Choose the number or range('1,n','1-n') to download or q' to quit:"
			input = raw_input('>>')
			return input
		elif mode == 2:
			print("no result, re-enter or 'q' to quit")
			input = raw_input('>>')
			return input
		elif mode == 3:
			print("The number is out of range, please choose correct number")
			input = raw_input(">>")
			return input
		elif mode == 4:
			print(">>Please input the correct number or range ('1,n','1-n') or 'q' to quit:")
			input = raw_input(">>")
			return input



	
	




