#=======================try to extract tweets contain sensitive words===========================#
#--------------------Words from the words list--------------------------#
#--------------The Structure of data is: ［sentence, keywords, user_id, tweet_id］ 

import os,pprint,pickle, re, random
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from get_saved_words import get_words

try:
    # UCS-4
    highpoints = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
except re.error:
    # UCS-2
    highpoints = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')


def process_statuses(uid):
	statuses_list = {}
	in_path = 'Data/'+uid+'/statuses_list.pickle'
	if os.path.exists(in_path):
		f = open(in_path,'rb')
		j = 0
		while True:
			try:
				statuses = pickle.load(f)
				for status in statuses:
					j += 1
					tweet = status.text
					if 

					sents = sent_tokenize(tweet)
					text = ""
					for sent in sents:
						#print("Sent: ", sent)
						sent_text = re.sub(r'RT\s@\w+:\s|@\w+\s|#|http://.*$|http://.*\s|https://.*$|https://.*\s|\n|\\U\w+', "", sent)
						sent_text = highpoints.sub("", sent_text)
						#print(sent_text)
						tokens = word_tokenize(sent_text)
						words = [w.lower() for w in tokens if w.isalpha() or w.isalnum()]
						stop_words = set(stopwords.words('english'))
						filtered_words = [w for w in words if not w in stop_words]
						statuses_list[sent] = filtered_words	#structure: key:integrate sentence, value: filtered_words 
			except EOFError:
				print(j)
				break
	#print("statuses_list: ", statuses_list)
	return statuses_list 

def  random_select():
	o_path = "part_sensitive_tweets"
	if not os.path.exists(o_path):
		os.makedirs(o_path)
	sen_words = os.listdir('Seperate_sensitive_tweets')
	for word in sen_words:
		in_path = "Seperate_sensitive_tweets/%s"%word
		sentence_list = []
		#-----------read the pickle file--------------#
		with open(in_path) as f:
			sentence_list = f.readlines()
		print("sentence_list: ", sentence_list)
		slenth = len(sentence_list)
		if slenth >= 100000:
			ext_num = round(slenth*0.001)
		elif slenth>=50000 and slenth<=100000:
			ext_num = round(slenth*0.005)
		elif slenth>=10000 and slenth<=50000:
			ext_num = round(slenth*0.01)
		elif slenth>=5000 and slenth<=10000:
			ext_num = round(slenth*0.05)
		elif slenth>=1000 and slenth<=5000:
			ext_num = round(slenth*0.1)
		elif slenth>=500 and slenth<=1000:
			ext_num = round(slenth*0.5)
		else: 
			ext_num = slenth
		rn = random.sample(range(0, slenth), ext_num)
		w = open(o_path+"/%s.txt"%word[0:-4],'a')   
		for n in rn:
			#w.writelines(bytes(sentence_list[n]+'\n','utf-8'))
			content = sentence_list[n]
			#print("content: ", content)
			w.writelines(content+'\n')
		
		
	return ""

if __name__ == "__main__":
	ids = os.listdir('Data')
	word_list = get_words()
	user_num = 1
	o_path = "Seperate_sensitive_tweets"
	if not os.path.exists(o_path):
		os.makedirs(o_path)
	for uid in ids:
		print(user_num, uid)
		user_num += 1
		statuses = {}
		statuses = process_statuses(uid)
		for key,value in statuses.items():
			#print("key, value: ", key, value)
			tag = 0
			keywords = []
			for candi_word in value:
				g = 0
				#print(candi_word)
				#--------------groups_bag version-------------#
				"""
				for word_list in word_lists:
					g += 1
					if not candi_word in word_list:
						continue
					tag = 1
					keywords.append(candi_word+str(g))
				"""
				#---------------wordset version---------------#
				if not candi_word in word_freq:		#if word_freq = 0, there's no picklefile for it
					continue
				tag = 1
				word_freq[candi_word] += 1
				keywords.append(candi_word)
			if tag == 1:
				to_write = "Sentence: "+key+'	'+"Keyword: "+str(keywords)+'\n'
				for k in keywords:
					fw = open(o_path+"/%s.txt"%k,'a')
					fw.write(to_write)
	sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
	print("word_freq: ")
	pprint.pprint(sorted_word_freq)
	random_select()
	print("***********All finished!!*********")
	
	
	
	

	
	
	
	