#! /usr/bin/env python3

import requests
import re

sessionhash = 'x'
replace_text = "."

# LOG IN

import requests

cookies = {
    'bymCommunity_sessionhash': sessionhash,
    'bymCommunity_lastvisit': '1639005858',
    'bymCommunity_lastactivity': '0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
}

response = requests.get('https://www.bym.de/forum', headers=headers, cookies=cookies)
contents=str(response.content)
m = re.search("profil\/(\d+)", contents)
userid = m.group(1)

params = (
    ('do', 'finduser'),
    ('userid', userid),
    ('contenttype', 'vBForum_Post'),
    ('showposts', '1'),
)

response = requests.get('https://www.bym.de/forum/search.php', headers=headers, params=params, cookies=cookies)
contents=str(response.content)


securitytoken = contents.split('SECURITYTOKEN = "')[1].split('"')[0]

# EXTRACT IDS

all_ids = []
all_ids.extend(re.findall("#post(\d+)", contents))
m = re.search("rel=\"next\" href=\"([^\"]+)", contents)


while (m is not None):
	next = m.group(1)
	next = next.replace("amp;", "")
	url = "https://www.bym.de/forum/"+next
	response = requests.get(url, cookies=cookies, headers=headers)
	contents=str(response.content)
	all_ids.extend(re.findall("#post(\d+)", contents))
	m = re.search("rel=\"next\" href=\"([^\"]+)", contents)

print("There are {} posts to delete.".format(len(all_ids)))
print("Test:" + all_ids[0])


# NUKE POSTS!

to_edit = []

for i in all_ids:
	
	data = {
		'do': 'deletepost',
		's': '',
		'securitytoken': securitytoken,
		'postid': i,
		'deletepost': 'delete',
		'reason': ''
		}

	response = requests.post('https://www.bym.de/forum/editpost.php', headers=headers, cookies=cookies, data=data)
	if "Du hast keine Rechte" in response.text:
		to_edit.append(i)
		    

## EDIT THREADS

for ids in to_edit:

    params = (
        ('do', 'updatepost'),
        ('p', ids),
        )

    data = {
        'reason': '',
        'message': replace_text,
        's': '',
        'securitytoken': securitytoken,
        'do': 'updatepost',
        'p': ids,
        }


    response = requests.post('https://www.bym.de/forum/editpost.php', params=params, headers=headers, cookies=cookies, data=data)
    
print("Done!")
