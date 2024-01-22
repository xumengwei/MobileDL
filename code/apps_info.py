# Get information on apps that use DL
# downloads, reviews, rankings, developers, check in & check out, category

# Comparison between DL-apps and non-DL-apps

import os
import time
import collections
import numpy as np

from basic_func import run_cmd, load_dict
from bs4 import BeautifulSoup

RAW_APK_PATH_NEW='../data/raw_apks_new/'
#HTML_PATH='../data/htmls/'
HTML_PATH_NEW='/mbdir/MobileDL/data/htmls/'#../data/htmls/'

html_path = '../data/dl_htmls/'
base_url = 'https://play.google.com/store/apps/details?id='

# apps that use dl in Jun. 2018
final_dl_pkgs = ['kr.co.daou.isa',]

# apps that use dl in Sep. 2018
new_final_dl_pkgs = ['kr.co.daou.isa',]

for app in new_final_dl_pkgs:
	print(app)
	cmd = 'wget ' + base_url + app + ' -O ' + os.path.join(html_path, app + '.html')
	run_cmd(cmd)
	time.sleep(1)

# count the downloads of DL-apps from Sep to Oct
old_html = HTML_PATH_NEW
new_html = '../data/dl_htmls'
def _get_downloads(s):
	return int(s.replace(',', '').replace('+', ''))
new_info = []
old_info = []
for app in new_final_dl_pkgs:
	with open(os.path.join(old_html, app + '.html')) as f:
		old_info.append(parse_html(f.read().decode('utf-8', 'ignore')))
	with open(os.path.join(new_html, app + '.html')) as f:
		new_info.append(parse_html(f.read().decode('utf-8', 'ignore')))

print(len(new_info), len(old_info))
new_downs = []
old_downs = []
new_reviews = []
old_reviews = []
for i in range(len(new_info)):
	if len(new_info[i]) < 4 or len(old_info[i]) < 4: continue
	old_downs.append(_get_downloads(old_info[i][4]))
	new_downs.append(_get_downloads(new_info[i][4]))
	old_reviews.append(int(old_info[i][0]))
	new_reviews.append(int(new_info[i][0]))

print(sum(new_downs), sum(old_downs), len(new_downs), sum(new_downs) - sum(old_downs))
print(sum(new_reviews), sum(old_downs), len(new_reviews), sum(new_reviews) - sum(old_reviews))

# find repeated
print([[item, count] for item, count in list(collections.Counter(new_final_dl_pkgs).items()) if count > 1])
print(len(final_dl_pkgs), len(new_final_dl_pkgs))
final_dl_pkgs = list(set(final_dl_pkgs))
new_final_dl_pkgs = list(set(new_final_dl_pkgs))
print(len(final_dl_pkgs), len(new_final_dl_pkgs))

def parse_html(content):
	try:
		soup = BeautifulSoup(content, "lxml")
		downloads = soup.find('meta', attrs={'itemprop': 'reviewCount'})['content']
		rate = soup.find('div', attrs={'class': 'BHMmbe'})
		rate = rate.get_text()
		spans = soup.find_all('span', attrs={'class': 'htlgb'})
		data = [s.get_text() for s in spans]
		data = [data[x] for x in range(len(data)) if x % 2 == 0]
		return [downloads, rate] + data
	except:
		return []

htmls = os.listdir(HTML_PATH_NEW)
print('total number:', len(htmls))
res = {}
cnt = 0
for h in htmls:
	html_file = os.path.join(HTML_PATH_NEW, h)
	pkg = h[:-4]
	with open(html_file) as f:
		res[pkg] = parse_html(f.read().decode('utf-8', 'ignore'))
	cnt += 1
	if cnt % 100 == 0:
		print('finish', cnt)

save_dict(res, '../data/html_res.pkl')

# example
#with open(os.path.join(HTML_PATH, 'com.qiyi.video.html')) as f:
#	print parse_html(f.read().decode('utf-8', 'ignore'))

# Compare DL-apps to non-DL-apps
meta_data = load_dict('../data/html_res.pkl')
meta_data = {k[:-1]: meta_data[k] for k in meta_data if len(meta_data[k]) > 0}
reviews = [int(meta_data[k][0]) for k in list(meta_data.keys()) if k not in new_final_dl_pkgs]
dl_reviews = [int(meta_data[k][0]) for k in list(meta_data.keys()) if k in new_final_dl_pkgs]

def _get_downloads(s):
	return int(s.replace(',', '').replace('+', ''))

downloads = [_get_downloads(meta_data[k][4]) for k in list(meta_data.keys()) if k not in new_final_dl_pkgs]
dl_downloads = [_get_downloads(meta_data[k][4]) for k in list(meta_data.keys()) if k in new_final_dl_pkgs]
ratings = [float(meta_data[k][1]) for k in list(meta_data.keys()) if k not in new_final_dl_pkgs]
dl_ratings = [float(meta_data[k][1]) for k in list(meta_data.keys()) if k in new_final_dl_pkgs]

def _get_size(s):
	s = s.replace(',', '').lower()
	if s.endswith('k'): return float(s[:-1]) / 1024
	elif s.endswith('m'): return float(s[:-1])
	elif s.endswith('g'): return float(s[:-1]) * 1024
	else: pass 
	size = [_get_size(meta_data[k][3]) for k in list(meta_data.keys()) if _get_size(meta_data[k][3]) != None and k not in new_final_dl_pkgs]
	dl_size = [_get_size(meta_data[k][3]) for k in list(meta_data.keys()) if k in new_final_dl_pkgs and _get_size(meta_data[k][3]) != None]

# Calculate the rankings
categories = os.listdir(RAW_APK_PATH_NEW)
rankings = []
total_downloads_top100 = 0
dl_downloads_top100 = 0
for c in categories:
	c_apps = os.listdir(os.path.join(RAW_APK_PATH_NEW, c))
	c_apps = [ca[:-4] for ca in c_apps if ca[:-4] in new_app_list]
	print(c, len(c_apps))
	c_downloads = [_get_downloads(meta_data[k][4]) for k in c_apps if k in list(meta_data.keys())]
	c_downloads = sorted(c_downloads, reverse=True)
	_dl_downloads = [_get_downloads(meta_data[k][4]) for k in c_apps if k in new_final_dl_pkgs]
	for d in _dl_downloads:
		r = np.mean([i for i, x in enumerate(c_downloads) if x == d])
		rankings.append(r)
		if r <= 100:
			dl_downloads_top100 += d
	total_downloads_top100 += sum(c_downloads[:100])

print(rankings)
print(np.median(rankings), np.mean(rankings))
print([r for r in rankings if r <= 100], len([r for r in rankings if r <= 100]))
print(dl_downloads_top100, total_downloads_top100, 1.0 * dl_downloads_top100 / total_downloads_top100)

downloads = {k : _get_downloads(meta_data[k][4]) for k in list(meta_data.keys())}
bar = sorted(downloads.values())[100]
dl_downloads = {k : _get_downloads(meta_data[k][4]) for k in list(meta_data.keys()) if k in new_final_dl_pkgs}
print(dl_downloads)

# Developers
temp = {app: meta_data[app][-2] for app in new_final_dl_pkgs}
dev = {}
for p in temp:
	if temp[p] not in dev: dev[temp[p]] = [p]
	else: dev[temp[p]].append(p)

print(len(list(dev.keys())))
print(len([k for k in list(dev.keys()) if len(dev[k]) > 1]))
for d in dev:
	if len(dev[d]) > 1:
		print(d, len(dev[d]), dev[d])

# checkin and checkout
inter_list = [p for p in old_app_list if p in new_app_list]
checkin = [p for p in inter_list if (p not in final_dl_pkgs and p in new_final_dl_pkgs)]
checkout = [p for p in inter_list if (p in final_dl_pkgs and p not in new_final_dl_pkgs)]
d1 = [p for p in final_dl_pkgs if p in new_final_dl_pkgs]
d2 = [p for p in inter_list if (p not in [final_dl_pkgs + new_final_dl_pkgs])]
print(len(checkin), len(checkout), len(d1), len(d2))
print(checkin)
print(checkout)

# category
categories = os.listdir(RAW_APK_PATH_NEW)
cc = {}
for c in categories:
	apps = os.listdir(os.path.join(RAW_APK_PATH_NEW, c))
	cc[c] = [app for app in apps if app[:-4] in new_final_dl_pkgs]
cc = sorted(list(cc.items()), key = lambda x: len(x[1]), reverse = True)
for c in cc:
	print(c)

