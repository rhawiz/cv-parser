import docx
import re
# import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

# java_path = "C:/Program Files/Java/jdk1.8.0_91/bin/java.exe"
# os.environ['JAVAHOME'] = java_path

cv = 0
email = 0
name = 0


def document_to_text(filename):
    if filename[-5:] == ".docx":
        doc = docx.Document(filename)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        global cv
        cv = '\n'.join(full_text)
        return cv
    elif filename[-4:] == ".pdf":
        return pdf_to_txt(filename)


def pdf_to_txt(file_path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(file_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    global cv
    cv = str
    return cv


def get_email(cv):
    match = re.search(r'[\w\.-]+@[\w\.-]+', cv)
    global email
    email = match.group(0)
    return email


# Convert document to text
document_to_text("resources\CV.docx")
print cv
