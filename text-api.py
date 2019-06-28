import requests
import time

sttime = "global"
fttime = "global"
sotime = "global"
fotime = "global"
snltime = "global"
fnltime = "global"
sktime = "global"
fktime = "global"

mimetype = ""

def mime(files):
    url = 'https://ecms-cis-tika.edap-cluster.com/detect/stream'
    headers = {'Cache-Control': 'no-cache'}
    m = requests.put(url, files=files, headers = headers)
    return m

def tika(files):
    global sttime
    global fttime
    sttime = time.time()
    url = 'https://ecms-cis-tika.edap-cluster.com/tika'
    headers = {'Content-Type' : mimetype,'Cache-Control': 'no-cache'}
    sttime = time.time()
    r = requests.put(url, files=files, headers = headers)
    fttime = time.time()
    return r

def xtika(files):
    global sotime
    global fotime
    url = 'https://ecms-cis-tika.edap-cluster.com/tika'
    headers1 = {'Content-Type' : 'application/pdf', 'X-Tika-PDFOcrStrategy': 'ocr_only', 'Cache-Control': 'no-cache'}
    sotime = time.time()
    r = requests.put(url, files=files, headers = headers1)
    fotime = time.time()
    return r

    
def nlpbuddy(text):
    global snltime
    global fnltime
    url = 'https://ecms-cis-nlpbuddy.edap-cluster.com/api/analyze'
    headers = {'Content-Type' : 'application/json'}
    data = {'text': text}
    snltime = time.time()
    r = requests.post(url, json=data)
    fnltime = time.time()
    return r

def klassify(text):
    global sktime
    global fktime
    url = 'https://ecms-cis-klassify.edap-cluster.com/classify'
    data = {"text": text}
    sktime = time.time()
    r = requests.post(url, json=data)
    fktime = time.time()
    return r
    
if __name__ == "__main__":     
    
    from tkinter import filedialog
    from tkinter import *
    import json
    #from tkinter import messagebox
    #messagebox.showinfo("Title", "a Tk MessageBox")

    root = Tk()
    #root.dirname = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory to scan')
    root.filename = filedialog.askopenfilename(parent=root,initialdir="/",title='Please select a file to scan')

    fin = open(root.filename, 'rb')
   
    
    #fin = open(r'C:\Users\mnguyen\Desktop\nocr.pdf', 'rb')
    files = {'files':fin}

    print ('Parsing File: ')
    m = mime(files)
    print (m.text)
    mimetype = m.text
    fin.seek(0)
    r = tika(files)
    print("Tika Took %s seconds ---" % (sttime - fttime))
    
    #Determine if PDF needs OCRing
    if len(r.text.strip())==0 and (mimetype == 'application/pdf'):
        fin.seek(0) # Move to the beginning of document
        r = xtika(files)
        print("Tika OCR Took %s seconds ---" % (sttime - fttime))


    #Need to parse JSON and Display only highest 3 results
    
    t = nlpbuddy(r.text)
    print("Text Summarization Took %s seconds ---" % (snltime - fnltime))
    t1 = t.json()
    
    a = t.json()    
    b = klassify(a['summary'])
    print("Classification Took %s seconds ---" % (sktime - fktime))

    #print("Summary: %t" % t1['summary'][:400])
    print(b.text)
    
    #TODO Determine MIME Type to handle different file types, Parse Json

    '''
    sttime = "global"
    fttime = "global"
    sotime = "global"
    fotime = "global"
    snltime = "global"
    fnltime = "global"
    sktime = "global"
    fktime = "global"
    '''
