import sys
from sklearn.externals import joblib
import json

km = joblib.load("cluster_model.pkl")
cv = joblib.load("vectorizer.pkl")

sample = "RT @murthaburke: Get up to $1,250 as Soon as the Next Business day! \nhttps://t.co/zoTcmHFvGP \n#blockchain #cryptocurrency #crypto #ethereum\u2026"
feat = cv.transform([sample])
relevant = km.predict(feat)[0]
print(relevant)
count = 0
with open(sys.argv[1]) as f:
	out_name = sys.argv[1].split(".")[0] + "_without_noise.txt"
	with open(out_name, "w+") as out:
		for line in f:
			try:
				text = json.loads(line)['text']
			except json.decoder.JSONDecodeError as e:
				continue
			feat = cv.transform([text])
			clust = km.predict(feat)[0]
			if clust == relevant:
				out.write(line)
			if not count % 1000:
				print(count)
			count += 1