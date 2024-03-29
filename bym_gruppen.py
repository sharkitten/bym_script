import requests
import hashlib
import random
import time
import re


def getGroupIDs(groups, cookies):
	groupmap = {}
	for g in groups:
		response = requests.get('https://www.bym.de/forum/'+g, cookies=cookies)
		contents=str(response.content)
		m = re.search("groupid=(\d+)", contents)
		groupmap[g] = m.group(1)
	return groupmap

username = 'username'
password = 'passwort'
replacetext = "."

md5pwd = hashlib.md5(password.encode()).hexdigest()

m = hashlib.md5()
m.update(password.encode('utf-8'))
md5pwsutf = m.hexdigest()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0'
}

params = (
    ('do', 'login'),
)

data = {
  'vb_login_username': username,
  'vb_login_password': '',
  'vb_login_password_hint': 'Kennwort',
  's': '',
  'securitytoken': 'guest',
  'do': 'login',
  'vb_login_md5password': md5pwd,
  'vb_login_md5password_utf': md5pwsutf
}

response = requests.post('https://www.bym.de/forum/login.php', headers=headers, params=params, data=data)

session_cookies = response.cookies
cookies = session_cookies.get_dict()

response = requests.get('https://www.bym.de/forum', headers=headers, cookies=cookies)
m = re.search("profil\/(\d+)", response.text)
userid = m.group(1)
securitytoken = response.text.split('SECURITYTOKEN = "')[1].split('"')[0]


params = (
    ('do', 'process'),
)

data = {
  'query': '',
  'titleonly': '0',
  'searchuser': username,
  'starteronly': '0',
  'exactname': '1',
  'searchdate': '0',
  'beforeafter': 'after',
  'sortby': 'dateline',
  'order': 'descending',
  'showposts': '1',
  'saveprefs': '1',
  'dosearch': 'Suchen',
  's': '',
  'securitytoken': securitytoken,
  'searchfromtype': 'vBForum:SocialGroupMessage',
  'do': 'process',
  'contenttypeid': '5'
}

response = requests.post('https://www.bym.de/forum/search.php', headers=headers, params=params, cookies=cookies, data=data)
contents=str(response.text)

# EXTRACT IDS

all_posts = []
all_posts.extend(re.findall("a href=\"(gruppen\/[^\"]+)", contents))
m = re.search("rel=\"next\" href=\"([^\"]+)", contents)

while (m is not None):
	next = m.group(1)
	next = next.replace("amp;", "")
	url = "https://www.bym.de/forum/"+next
	response = requests.get(url, cookies=cookies, headers=headers)
	contents=str(response.content)
	all_posts.extend(re.findall("a href=\"(gruppen\/[^\"]+)", contents))
	m = re.search("rel=\"next\" href=\"([^\"]+)", contents)
	time.sleep(3)

groupmap = getGroupIDs(set(all_posts[1::2]), cookies)
print(groupmap)
all_posts = [(all_posts[x].split('#')[1][8:],groupmap[all_posts[x+1]]) for x in range(0,len(all_posts),2)]
random.shuffle(all_posts)

print("There are {} posts to delete.".format(len(all_posts)))

# NUKE POSTS!

to_edit = []

for i in range(len(all_posts)):
	print(all_posts[i])
	data = {
	'deletemessage': 'soft',
	'reason': '',
	's': '',
	'securitytoken': securitytoken,
	'gmid': all_posts[i][0],
	'do': 'deletemessage',
	'groupid': all_posts[i][1],
	'page': '0'
}

	response = requests.post('https://www.bym.de/forum/group.php', headers=headers, cookies=cookies, data=data)
	print("Beitrag {} in Gruppe {} wurde gelöscht (hoffentlich).".format(all_posts[i][0], all_posts[i][1]))
	time.sleep(3)
	if (i>0 and i%50==0):
		print(str(i+1)+' Beiträge verarbeitet')
