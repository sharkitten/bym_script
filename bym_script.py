import requests
import hashlib
import random
import time
import re

username = 'username'
password = 'password'
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

cookies = response.cookies.get_dict()

response = requests.get('https://www.bym.de/forum', headers=headers, cookies=cookies)

userid = re.search("profil\/(\d+)", response.text).group(1)
securitytoken = response.text.split('SECURITYTOKEN = "')[1].split('"')[0]


params = (
    ('do', 'process'),
)

data = [
  ('query', ''),
  ('titleonly', '0'),
  ('searchuser', username),
  ('starteronly', '0'),
  ('exactname', '1'),
  ('tag', ''),
  ('childforums', '1'),
  ('replyless', '0'),
  ('replylimit', ''),
  ('searchdate', '0'),
  ('beforeafter', 'after'),
  ('sortby', 'dateline'),
  ('order', 'descending'),
  ('showposts', '1'),
  ('dosearch', 'Suchen'),
  ('searchthreadid', ''),
  ('s', ''),
  ('securitytoken', securitytoken),
  ('searchfromtype', 'vBForum:Post'),
  ('do', 'process'),
  ('contenttypeid', '1'),
]

response = requests.post('https://www.bym.de/forum/search.php', headers=headers, params=params, cookies=cookies, data=data)

# EXTRACT IDS

all_ids = []
all_ids.extend(re.findall("#post(\d+)", response.text))
m = re.search("rel=\"next\" href=\"([^\"]+)", response.text)


while (m is not None):
	next = m.group(1).replace("amp;", "")
	response = requests.get('https://www.bym.de/forum/'+next, cookies=cookies, headers=headers)
	all_ids.extend(re.findall("#post(\d+)", response.text))
	m = re.search("rel=\"next\" href=\"([^\"]+)", response.text)
	time.sleep(3)

print("There are {} posts to delete.".format(len(all_ids)))

random.shuffle(all_ids)


# NUKE POSTS!

to_edit = []

for i, val in enumerate(all_ids):
	
	data = {
		'do': 'deletepost',
		's': '',
		'securitytoken': securitytoken,
		'postid': val,
		'deletepost': 'delete',
		'reason': ''
		}

	response = requests.post('https://www.bym.de/forum/editpost.php', headers=headers, cookies=cookies, data=data)
	time.sleep(3)
	if "Du hast keine Rechte" in response.text:
		to_edit.append(val)
		print(str(val)+' kann nicht gelöscht werden')
	if (i>0 and i%50==0):
		print(str(i+1)+' Beiträge verarbeitet')
		    

## EDIT THREADS

for ids in to_edit:

    params = (
        ('do', 'updatepost'),
        ('p', ids),
        )

    data = {
        'reason': '',
        'message': replacetext,
        's': '',
        'securitytoken': securitytoken,
        'do': 'updatepost',
        'p': ids,
        }


    response = requests.post('https://www.bym.de/forum/editpost.php', params=params, headers=headers, cookies=cookies, data=data)
    time.sleep(3)
    
print("Done!")
