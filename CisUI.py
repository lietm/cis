#from Services import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from collections import Counter
import mimetypes
import json

import requests
import time

def tika(files):
    url = 'https://ecms-cis-tika.edap-cluster.com/tika/form'
    headers = {'Cache-Control': 'no-cache'}
    s = time.time()
    r = requests.post(url, files=files, headers = headers)
    f = time.time()
    return(r, f-s)

def xtika(files):
    url = 'https://ecms-cis-tika.edap-cluster.com/tika'
    headers = {'Content-Type' : 'application/pdf', 'X-Tika-PDFOcrStrategy': 'ocr_only', 'Cache-Control': 'no-cache'}
    s = time.time()
    r = requests.put(url, files=files, headers = headers) #post
    f = time.time()
    return(r, f-s)

def nlpbuddy(text):
    url = 'https://ecms-cis-nlpbuddy.edap-cluster.com/api/analyze'
    #headers = {'Content-Type' : 'application/json'}
    data = {'text': text}
    s = time.time()
    r = requests.post(url, json=data)
    f = time.time()
    return(r, f-s)

def klassify(text):
    url = 'https://ecms-cis-klassify.edap-cluster.com/classify'
    data = {'text': text}
    s = time.time()
    r = requests.post(url, json=data)
    f = time.time()
    return(r, f-s)

def getLabel(label):
    x = label[label.index('_')+1:label.index('_')+5]
    y = x.replace('_','')
    url = 'https://developer.epa.gov/api/index.php/records/api_records?filter=Record_Schedule_Number,cs,' + y
    r = requests.get(url)
    q = r.json()
    return q['records'][0]['Schedule_Title']

class Base(tk.Frame):
	
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		self.master.title('EZier Records')
		self.master.resizable(0,0)      
		#self.master.geometry('480x300') #width-height
		self.master.config(bg='black')
		self.filename = ''
		self.schedule_list = ['','','']
		self.summary = 'Hello How are You'
		self.keywords = ''
		self.information = '' 
		self.fin = bin
		self.files = {}
		self.recordlabel = ''

		#main containers
		self.top_box = tk.Frame(self.master, bd=1, bg='black')
		self.summary_box = tk.LabelFrame(self.master, text='Summary', padx=5, pady=5, bg='black', fg='white')
		self.keywords_box = tk.LabelFrame(self.master, text='Keywords', padx=5, pady=5, bg='black', fg='white')
		self.info_box = tk.LabelFrame(self.master, text='Information', padx=5, pady=5, bg='black', fg='white')
		
		
		self.top_box.grid(row=0, sticky="nsew")
		self.summary_box.grid(row=3, sticky='nsew')
		self.keywords_box.grid(row=2, sticky='nsew')
		self.info_box.grid(row=1, sticky='nsew')
		
		
		# widgets for the top_box
		self.top_box.grid_rowconfigure(1, weight=1)
		self.top_box.grid_columnconfigure(2, weight=1)

		self.upload_button = tk.Button(self.top_box, text="Upload", bg='DarkOrchid4', fg='white')
		self.upload_button.grid(row=0, column=0)
		
		self.boxlabel = tk.Label(self.top_box, width=50, text='Recommended Schedules')
		self.boxlabel.grid(row=0, column=1)     
		self.schedule_box = ttk.Combobox(self.top_box, width=50, values=self.schedule_list, state='readonly')
		self.schedule_box.grid(row=1, column=1)

		self.validate_button = tk.Button(self.top_box, text="Validate", command=self.goodbye, bg='plum')
		self.validate_button.grid(row=0, column=2)

		#text display for summary, keywords, info
		self.summary_message = tk.Message(self.summary_box, text=self.summary, anchor='w', justify='left', bg='black', fg='white')
		self.keywords_message = tk.Message(self.keywords_box, text=self.keywords, anchor='w', justify='left', bg='black', fg='white')
		self.info_message = tk.Message(self.info_box, text=self.information, anchor='w', justify='left', bg='black', fg='white')

		self.summary_message.pack(fill='both')
		self.keywords_message.pack(fill='both')
		self.info_message.pack(fill='both')
		
		#bind function to click
		self.upload_button.bind('<Button-1>', self.update_text)
		
		#bind resizing, might not need
		self.master.bind('<Configure>', self.update_mess)
		#self.info_box.bind('<Button-1>', self.speak)
		self.summary_message.bind('<Button-1>', lambda event: self.talk(self.summary))
		self.keywords_message.bind('<Button-1>', lambda event: self.talk(self.keywords))
		self.info_message.bind('<Button-1>', lambda event: self.talk(self.information))
		
		from win32com.client import Dispatch
		self.voice = Dispatch("SAPI.SpVoice")

	def goodbye(self):
		if len(self.summary)<2:
			self.voice.Speak('Please Upload a Document')
		else:
			self.voice.Speak('Your record was sent to the Enterprise Content Management System')
		
	def talk(self, text):
		if len(text)<2:
			self.voice.Speak('Please Upload a Document')
		else:
			self.voice.Speak(text)
	
	def update_mess(self,event):
		self.info_message.config(width=self.master.winfo_width())
		self.summary_message.config(width=self.master.winfo_width())
		self.keywords_message.config(width=self.master.winfo_width())
		#self.master.update()                

	      
	def update_text(self, event):
		self.filename =  filedialog.askopenfilename(parent=root,initialdir="C:/Users/mnguyen/Desktop",title='Please select a file to scan')
		
		#run voice command here
		self.fin = open(self.filename, 'rb')
		self.files = {'files':self.fin}

		self.mimetype = mimetypes.MimeTypes().guess_type(self.filename)[0]
		self.summary_message.config(text=self.mimetype)

	
		e0,t0 = tika(self.files)
		
		# or (mimetype == 'application/vnd.ms-excel') or (mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		
		eseconds = abs(round(t0,2))
		self.information = 'Text Extraction Took ' + str(eseconds) + ' seconds' + '\n'
		
		if len(e0.text.strip()) == 0 and self.mimetype =='application/pdf':
			self.fin.seek(0)
			self.files = {'files':self.fin}
			e0,t0 = xtika(self.files)
			eseconds = abs(round(t0,2))
			self.information = 'Text Extraction with OCR Took ' + str(eseconds) + ' seconds' + '\n'

		#run voice command here 
		#if len(r.text.strip())==0: quit()

		(e1,t1) = nlpbuddy(e0.text)
		a = e1.json()['summary']
		(e2,t2) = klassify(a)
		
		#run voice command here
		d = Counter(e2.json()['scores'])
		self.schedule_list.clear()

		for k,v in d.most_common(3):
			label = getLabel(k)
			self.schedule_list.append(k + ': ' + label)
		size = self.fin.seek(0,2)
		self.fin.close()
		self.schedule_box.config(value = self.schedule_list)
		self.schedule_box.current(0)

		#run voice command here

		sseconds = abs(round(t1,2))
		cseconds = abs(round(t2,2))

		self.information += 'Document Summarization Took ' + str(sseconds) + ' seconds' + '\n'
		self.information += 'Classification Took ' + str(cseconds) + ' seconds' + '\n'
		self.information += 'Total Time took to process of ' + str(size) + ' bits: ' + str(abs(round(t0+t1+t2,2))) + ' seconds'
		#run voice command here

		self.summary = e1.json()['summary']
		self.keywords = e1.json()['keywords']


		self.summary_message.config(text=self.summary)
		self.keywords_message.config(text=self.keywords)
		self.info_message.config(text=self.information)


if __name__ == "__main__":

	
	#start the voice service first
	root = tk.Tk()
	Base(master=root)
	root.mainloop()


