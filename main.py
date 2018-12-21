import json
import urllib
import time
import urllib.request

jsonUrl = "https://api.github.com/users/kuhnchris/events"

def readGithubUrl(url):
    ret = urllib.request.urlopen(url)
    jsonRet = json.load(ret)
    next_link = ""
    if "Link" in ret.headers:
        for pair in ret.headers["Link"].split(","):
            link, val = pair.split(';', 1)
            if val.split('"')[1] == "next":
                next_link = link.split('<')[1].split(">")[0]
        print("links found: "+ret.headers["Link"])
        print("cut link-next_link: "+next_link)
    # print(ret.headers)
    for obj in jsonRet:
        if "payload" in obj:
            if "issue" in obj["payload"]:
                if "state" in obj["payload"]["issue"]:
                    status = obj["payload"]["issue"]["state"]
                else:
                    status = "???"
                print(f'({status}) {obj["repo"]["name"]} - #{obj["payload"]["issue"]["number"]} - {obj["payload"]["issue"]["title"]} ({obj["payload"]["issue"]["url"]})')

    print(f'DEBUG: {jsonRet}')
    expDate = time.ctime(int(ret.headers["X-RateLimit-Reset"]))
    print(f'DEBUG: {ret.headers["X-RateLimit-Remaining"]} of {ret.headers["X-RateLimit-Limit"]} attempts remaining, expiring {expDate}')

    if next_link != "":
        readGithubUrl(next_link)


readGithubUrl(jsonUrl)
