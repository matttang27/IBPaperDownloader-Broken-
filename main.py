import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)
check1 = time.perf_counter()
counter = 0

#Folder path to download to (e.g "C:/IBPAPERS/")
FOLDERPATH = './Papers/PSYCHOLOGY_SL/'
#Link to download from
DOWNLOADLINK = 'https://www.ibdocuments.com/IB%20PAST%20PAPERS%20-%20SUBJECT/Group%203%20-%20Individuals%20and%20Societies/Psychology_SL/'


def get_url_paths(ourl, ext='', params={}):
    response = requests.get(ourl, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    urls = ["https://www.ibdocuments.com/" + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    urls = list(filter(lambda url:len(url) > len(ourl), urls))
    return urls

def loadExam(url,num):
    name = url.split('/')[-2].replace("%20"," ")

    echeck1 = time.perf_counter()
    Path("{}{}".format(FOLDERPATH,name)).mkdir(parents=True, exist_ok=True)
    pcheck1 = time.perf_counter()
    papers = get_url_paths(url,'pdf')
    pcheck2 = time.perf_counter()
    logging.info("{: >30}{}: {:10.4f}".format("Get url paths Exam # ",num,pcheck2-pcheck1))
    paperthreads = list()
    for j in range(len(papers)):
        t = threading.Thread(target=loadPaper, args=(papers[j],j,name,num))
        paperthreads.append(t)
        t.start()
    for j in range(len(papers)):
        paperthreads[j].join()
    echeck2 = time.perf_counter()
    logging.info("{: >30}{}: {:10.4f}".format("Total time for Exam # ",i,echeck2-echeck1))


def loadPaper(url,num,name,count):
    
    if ("French" in url or "Spanish" in url or "German" in url):
        return
    rcheck1 = time.perf_counter()
    pdf_resp = requests.get(url)
    rcheck2 = time.perf_counter()
    logging.info("{: >30}{}-{}: {:10.4f}".format("Get url paths Paper # ",count,num,rcheck2-rcheck1))
    global counter
    counter += 1
    wcheck1 = time.perf_counter()
    with open("{}{}/{}".format(FOLDERPATH,name,url.split("/")[-1]), "wb") as f:
        f.write(pdf_resp.content)
    wcheck2 = time.perf_counter()
    logging.info("{: >30}{}-{}: {:10.4f}".format("Save paper # ",count,num,wcheck2-wcheck1))


exams = get_url_paths(DOWNLOADLINK,"/")
check2 = time.perf_counter()
logging.info("{: >30}{:10.4f}".format("get url paths for main: ",check2 - check1))




examthreads = list()
for i in range(len(exams)):
    x = threading.Thread(target=loadExam, args=(exams[i],i))
    examthreads.append(x)
    x.start()
    
for i in range(len(exams)):
    examthreads[i].join()
        

check3 = time.perf_counter()
logging.info("{: >30}{:10.4f}".format("TOTAL TIME: ",check3-check1))
logging.critical("Download completed! Total pdfs saved: {}".format(counter))