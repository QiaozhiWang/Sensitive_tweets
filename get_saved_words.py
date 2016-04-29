import os, re
import pprint as pp

def get_words():
	f = open("save_words.txt", 'r')
	lines = [line.rstrip('\n') for line in f]
	#pp.pprint(lines)
	word_list = []
	for l in lines:
		m = re.search(r'(\(\')(\w+)(\'(.*))',l)
		word_list.append(m.group(2))
	#pp.pprint(word_list)
	return word_list