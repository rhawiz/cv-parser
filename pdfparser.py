import os
import re

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

from time import sleep

BASE_DIR = "cv"

def get_email(text):
    match = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return match

def pdf_to_text(pdf_path):
    fp = file(pdf_path, 'rb')
    res_mgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(res_mgr, retstr, codec=codec, laparams=laparams)
    interp = PDFPageInterpreter(res_mgr, device)
    for page in PDFPage.get_pages(fp):
        interp.process_page(page)
        content = retstr.getvalue()

    return content


def convert():
    for subdir, dirs, files in os.walk(BASE_DIR):
        for f in files:
            pdf_path = os.path.abspath(os.path.join(subdir, f))
            text = pdf_to_text(pdf_path)
            id = f.split('.')[0]
            category = subdir
            print id


if __name__ == "__main__":
    convert()
