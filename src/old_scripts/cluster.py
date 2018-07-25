import json
import numpy as np
from sklearn import cluster
"""Data used to build model:
$head -n 20000 appa.out.text > sample.txt
"""

tweets = {}
keywords_general = set(("cryptocurrency", "crypto", "currency", "altcoin", "blockchain", "decentralized", "million", "millions", "coinbase", "trend", "expand", "trending", "expanding", "payment", "payments", "market", "markets", "invest", "investing"))
keywords_clear = set(("bitcoin", "bitcoins", "btc", "bitcoincash", "bch", "ethereum", "eth", "xrp", "litecoin", "ltc"))
keywords_unclear = set(("ripple", "ether", "cash", "coin"))
handles = set(("@ethereum", "@bitcoin", "@bitcoincash", "@ripple", "@litecoin"))
uids = set(("2312333412", "357312062", "225710587", "1051053836", "385562752"))

def sanitize(text):
	words = text.split()
	final = []
	hashtags = []
	for word in words:
		if "http" not in word:
			if "#" in word:
				clean = word.replace("#", "").lower()
				clean = "".join([x for x in clean if x.isalpha()])
				hashtags.append(clean)
				if clean != "":
					final.append(clean)
			elif "@" in word:
				clean = word.lower()
				if clean != "":
					final.append(clean)
			elif "$" in word:
				final.append("$")
			else:
				clean = word.lower()
				clean = "".join([x for x in clean if x.isalpha()])
				if clean != "":
					final.append(clean)

	print(words, final, hashtags)
	return final, hashtags
def gen_features(t_tup):
	word_list = t_tup[0]
	tags = t_tup[1]
	uid = t_tup[2]
	features = [0] * 6
	tag_weight = 0.5
	for i in range(0, len(word_list)):
		if word_list[i] in keywords_general:
			features[0] += 1
		if word_list[i] in keywords_clear:
			features[1] += 1
		if word_list[i] in keywords_unclear:
			features[2] += 1
		if word_list[i] in handles:
			features[3] += 1
		if word_list[i] == "$":
			features[5] += 1
	for i in range(0, len(tags)):
		if tags[i] in keywords_general:
			features[0] += tag_weight
		if tags[i] in keywords_clear:
			features[1] += tag_weight
		if tags[i] in keywords_unclear:
			features[2] += tag_weight
		if tags[i] in handles:
			features[3] += tag_weight
	if str(uid) in uids:
		features[4] += 1
	features[5] = float(t_tup[3]['retweets'])
	return features

clusts = None
row_to_id = {}
#File is newline delimited json objects
with open("sample.txt") as f:
	for line in f:
		try:
			t = json.loads(line)
			print(t['text'])
			if t['text']:
				words, tags = sanitize(t['text'])
				tweets[t["id"]] = (words, tags, t['user_id'], t)
		except json.decoder.JSONDecodeError as e:
			print("no")
	features = np.zeros((len(tweets), 6))
	count = 0
	for t in tweets:
		row_to_id[count] = t
		features[count, 0] = t
		x = gen_features(tweets[t])
		for i in range(0, len(x)):
			features[count, i] = x[i]
		count += 1
	print(len(row_to_id))
	mbk = cluster.MiniBatchKMeans(n_clusters=2)
	clusts = mbk.fit_predict(features)

with open("class_0.txt", "w+") as out0:
	with open("class_1.txt", "w+") as out1:
		for i in range(len(clusts)):
			t = row_to_id[i]
			print(tweets[t][3], tweets[t][2])
			if clusts[i] == 0:
				out0.write(tweets[t][3]['text'] + "\n" + ",".join(tweets[t][0]) + "\n")
				for j in range(0, 6):
					out0.write(str(features[i][j]) + ",")
				out0.write("\n")
			else:
				out1.write(tweets[t][3]['text'] + "\n" + ",".join(tweets[t][0]) + "\n")
				for j in range(0, 6):
					out1.write(str(features[i][j]) + ",")
				out1.write("\n")
				
