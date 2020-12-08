import tabula
import time

t0 = time.time()
tabula.convert_into("027_CSE_6_SEM.pdf", "output.csv", pages='all', area=[197.259375,26.7975,739.164375,1189.51125], output_format='csv', guess=False)
t1 = time.time()

print "PDF processed in {} seconds".format(t1-t0)