import os,re,sys,csv,ast
import pprint as pp
import numpy as np

file_len = []
fs = open("save_words.txt", 'r')
saved_words = [line.rstrip('\n') for line in fs]
#pp.pprint(lines)
word_list = []
for sw in saved_words:
	m = re.search(r'(\(\')(\w+)(\'(.*))',sw)
	word_list.append(m.group(2))

for word in word_list:
	#-------------Put in one sentence-------------------#
	f = open("Seperate_sensitive_tweets/%s.txt"%word,'r')
	lines = [line.rstrip('\n') for line in f]
	#pp.pprint(lines)
	i = 0
	while True:
		try:	
			if lines[i] == '':
				lines.remove(lines[i]);
				#print("1: ", lines[i])
			elif not re.search(r'Sentence\:\s',lines[i]):
				lines[i-1] = lines[i-1]+' '+lines[i]
				lines.remove(lines[i])
				#print("2: ", lines[i])
			else:
				i += 1
		except IndexError:
			#print("******** Finish processing one file ! *********")
			break
	#pp.pprint(lines)
	#------------Delete duplicated tweets-------------------#
	uniqlines = list(set(lines))
	#pp.pprint(uniqlines)

	#-------------Write to the new file----------------#
	o_path = "Processed_seperate_tweets"
	if not os.path.exists(o_path):
		os.mkdir(o_path)
	f_out =  open(o_path+"/%s.txt"%word, 'w')
	f_out.writelines(["%s\n" %item  for item in list(uniqlines)])

	#----------------Rank and select based on rank--------------#
	weight_list = []		#store keyword length of each sentence
	for l in range(0, len(uniqlines)):
		try:
			k = re.search(r'(Keyword\:\s)(\[(.*)\])', uniqlines[l])
			new_k = ast.literal_eval(k.group(2))
			weight_list.append(len(new_k))
		except:
			print(sys.exc_info()[0], l, uniqlines[l])
			continue
	#print(sorted_kw_dic)
	weight_list = np.array(weight_list)
	wsum = np.sum(weight_list)
	a = len(weight_list)
	file_len.append(a)
	#print("****Length of file %s is %s"%(word, a))
	norm = weight_list/float(wsum)
	select = np.random.choice(a, 10, p=norm)
	#print(select)

print("file_len: ", file_len)




