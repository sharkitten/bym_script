#! /usr/bin/env python3


from bs4 import BeautifulSoup
import requests

# LOG IN

import requests

cookies = {
    '_sp_enable_dfp_personalized_ads': 'false',
    '_sp_v1_uid': '1:998:f1edc63e-6619-4df7-8fa9-76aab0133f45',
    '_sp_v1_data': '2:421501:1637928764:0:994:0:994:0:0:_:-1',
    '_sp_v1_ss': '1:H4sIAAAAAAAAAItWqo5RKimOUbLKK83J0YlRSkVil4AlqmtrlXTgyqKxMvJADIPaWFwGkC6BZCWRLsOrLBYAPu-qjekAAAA%3D',
    '_sp_v1_opt': '1:login|true:last_id|11:',
    '_sp_v1_consent': '1!1:1:1:0:0:0',
    '_sp_v1_csv': 'null',
    '_sp_v1_lt': '1:',
    'consentUUID': '78e88833-62bb-4ce1-90a5-6b5ac6ec7e4a_1_2',
    'euconsent-v2': 'CPQzM5jPQzM5jAGABCDEB4CgAP_AAAHAAAYgHsgZBDoUTGHAUXh4QvsAGYQTEEQUAGACCBCAIiABAAAAMDQAkgAAsASAAAACAQIAIBIBAAAECAAEAEAAAAAEAAEgAAAAhAAIIAJAABEAAAAAAAICAAAAAAAIAAARAAAAmQAAA0KEAGAAAEAQYAAAgAAAAAAEAAEAAAAAAIIAAAEQkB0ACoAGQAPAAgABkADQAHkARABFACYAE8AN4AcwA_ACGAEsAKUAW4AwwBqgD9AMUAbgA4gB6AENgJEAUiAvMBpwQAGACQAZoCVh0CwACoAGQAQAAyABoADwAH0ARABFACYAE-ALgAugBfADEAG8AOYAfgBDACWAEwAKUAWIAtwBhgDRAH6ARYAsQBaQC6gGKANwAcQA9ACGwEXgJBASIAvMBfQDEgGWANEAacA1UcAIAAuACQAZoBBQCEAGBANeAlYNAGAC4AIYAgoBaQEiAKREQAwBDAJEAUiIAAgAkGQAgAmALzGAAQCxCoAoATAAuAFpASCAvMUABAIKQgIAAZACYAFwAL4AYgA3gCxALSAYoA9ACQQEiALaAYkA0QBqpAAEAQUAsRKAmABkAHgARAAmABcAC-AGIAQwApQBbgDVALSAXUAxQBuAEXgJEAXmAywkADAAuAa8BKxSA6ABUADIAIAAZAA0AB5AEQARQAmABPAC-AGIAOYAfgBDAClAFiALcAaIA1QB-gEWAMUAbgA9ACLwEiALzAX0AywoAHAAuACQAnYBYgC6gGvAaIAA.YAAAAAAAAAAA',
    'sp_ga': '1',
    'euconsent-addtl': '1~',
    'bymCommunity_sessionhash': '826c9b9fcd6623c94025d49763b1481a',
    'bymCommunity_lastvisit': '1638981054',
    'bymCommunity_lastactivity': '0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'Referer': 'https://www.bym.de/forum/profil/91909-nameschonweg.html',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}

params = (
    ('do', 'finduser'),
    ('userid', '91909'),
    ('contenttype', 'vBForum_Post'),
    ('showposts', '1'),
)

response = requests.get('https://www.bym.de/forum/search.php', headers=headers, params=params, cookies=cookies)



# EXTRACT IDS

list_of_lists = []

for page in range(1, 2):

    params = (
        ('searchid', '9827916'),
        ('pp', ''),
        ('page', str(page)),
        )   
    
    response = requests.get('https://www.bym.de/forum/search.php', headers=headers, params=params, cookies=cookies)

    soup = BeautifulSoup(response.text, "html.parser")
    selector = 'div > h3 > a'
    hrefs = soup.select(selector)
    post_ids = [href['href'][-10:] for href in hrefs]
    if len(post_ids) == 0:
        continue
    else:
        list_of_lists.append(post_ids)
    

all_ids = [item for sublist in list_of_lists for item in sublist]

print("There are {} posts to delete.".format(len(all_ids)))
print("Test:" + all_ids[0])



# SAVE POSTS

for i in all_ids:
        
    text = soup.find(id=("post_message_" + i))
    with open(r"C:\Users\Anwender\Desktop\bym\bymmel.txt", "a") as file:
      file.write(str(text.text) + "\n")




# NUKE POSTS!

for i in all_ids:
	

	data = {
		'do': 'deletepost',
		's': '',
		'securitytoken': '1638981233-876eef6645e623697516a233ed2f3cec0aced820',
		'postid': i,
		'deletepost': 'delete',
		'reason': ''
		}

	response = requests.post('https://www.bym.de/forum/editpost.php', headers=headers, cookies=cookies, data=data)
    
    

# EXTRACT THREAD IDS

list_of_lists_threads = []

for page in range(1, 2):
  
    params = (
        ('searchid', '9827916'),
        ('pp', ''),
        ('page', str(page)),
        )   
    
    response = requests.get('https://www.bym.de/forum/search.php', headers=headers, params=params, cookies=cookies)

    soup = BeautifulSoup(response.text, "html.parser")
    selector = 'div > h3 > a'
    hrefs = soup.select(selector)
    thread_ids = [href['href'][-10:] for href in hrefs]
    if len(post_ids) == 0:
        continue
    else:
        list_of_lists_threads.append(thread_ids)
    

all_thread_ids = [item for sublist in list_of_lists for item in sublist]

print("There are {} threads to edit.".format(len(all_thread_ids)))
print("Test:" + all_thread_ids[0])



# EDIT THREADS

for ids in all_thread_ids:

    params = (
        ('do', 'updatepost'),
        ('p', ids),
        )

    data = {
        'reason': '',
        'title': '',
        'message_backup': '-',
        'message': '---',
        'wysiwyg': '0',
        'iconid': '5',
        'sbutton': '%C4nderungen speichern',
        'signature': '1',
        'parseurl': '1',
        'emailupdate': '0',
        's': '',
        'securitytoken': '1638981233-876eef6645e623697516a233ed2f3cec0aced820',
        'do': 'updatepost',
        'p': ids,
        'posthash': 'c0208335d8d0056c5f5b6527621cee61',
        'poststarttime': '1638957433'
        }


    response = requests.post('https://www.bym.de/forum/editpost.php', headers=headers, params=params, cookies=cookies, data=data)
    
print("Done!")
