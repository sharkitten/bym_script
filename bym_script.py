#! /usr/bin/env python3

import requests
import re

pwd = "x"
sessionhash = "x"
userid = "x"
replace_text = ".a"

# LOG IN

import requests

cookies = {
    "bymCommunity_lastactivity": "0", 
    "bymCommunity_lastvisit": "1638478923", 
    "bymCommunity_password": pwd,
    "bymCommunity_sessionhash": sessionhash,
    "bymCommunity_userid": userid
}


params = (
    ('do', 'finduser'),
    ('userid', '117007'),
    ('contenttype', 'vBForum_Post'),
    ('showposts', '1'),
)

response = requests.get('https://www.bym.de/forum/search.php', params=params, cookies=cookies)
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
	response = requests.get(url, cookies=cookies)
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

	response = requests.post('https://www.bym.de/forum/editpost.php', cookies=cookies, data=data)
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


    response = requests.post('https://www.bym.de/forum/editpost.php', params=params, cookies=cookies, data=data)
    
print("Done!")

