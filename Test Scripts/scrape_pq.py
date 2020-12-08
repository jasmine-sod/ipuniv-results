import pdfquery
import re
import time
from pdfquery.cache import FileCache

pdf = pdfquery.PDFQuery("028_ECE_6_SEM.pdf",parse_tree_cacher=FileCache("/tmp/"))
t0 = time.time()
pdf.load()
t1 = time.time()

print "Loaded in {} seconds".format(t1-t0)

data = pdf.extract([
    ('clg_code', 'LTPage:contains("SCHEME OF EXAMINATIONS")')
])

pages = []

for page in data['clg_code']:
    pages.append(page.get('pageid'))

print pages