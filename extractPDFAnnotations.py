from PyPDF2 import PdfFileReader
import subprocess
from pathlib import Path
import markdown2
import sys

filename = str(sys.argv[1])
reader = PdfFileReader(filename)
finalNote = '<h2> Notes </h2><br>'


pageNum=0
for page in reader.pages:
    pageNum+=1
    if "/Annots" in page:
        for annot in page["/Annots"]:
            subtype = annot.get_object()["/Subtype"]
            if subtype == "/Text":
                finalNote+='''Page:'''+ str(pageNum)+''' <a href="''' + filename  + '''#page=''' + str(pageNum) + '''">''' + annot.get_object()["/Contents"] +'''</a><br>'''
           
            if subtype == "/FreeText":
                finalNote+='''Page:'''+ str(pageNum)+''' <a href="''' + filename  + '''#page=''' + str(pageNum) + '''">''' + annot.get_object()["/Contents"] +'''</a><br>'''


## use pdfannots to extract the highlights
subprocess.call(['pdfannots', filename, '-s','highlights', '-o', 'pdfAnnots_foo.txt'])
txt = Path('pdfAnnots_foo.txt').read_text()

## replace all the page 1, page 3 , etc from output to be urls instead. Assume maximum of 1000 pages
## Has to be reversed otherwise Page 100 might be mistaken for Page 10 or Page 1
for i in reversed(range(1000)):
    string = "Page %d"%(i+1)
    string_updated =''' <a href="''' + filename  + '''#page=''' + '''%d">Page-%d'''%(i+1,i+1) + '''</a><br>'''
    txt = txt.replace(string, string_updated)


finalNote += "<br>"+markdown2.markdown(txt)


print(finalNote)