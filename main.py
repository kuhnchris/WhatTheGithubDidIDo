import json
import urllib
import time
import urllib.request
import argparse
from graphqlclient import GraphQLClient
from config import TOKEN

# Python program to print
# colored text and background
class colors:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

parser = argparse.ArgumentParser(description='Fetches (and processes) github events')
parser.add_argument('-e','--readUserEvents', help="read all events from user specified", action="store_true", default='True')
parser.add_argument('-s','--readIssueStatus', help="read all status from connected issues", action="store_true", default='True')
parser.add_argument('--readUserEventFile', help="file to read a stored --readUserEvent step from", default='')
parser.add_argument('--writeUserEventFile', help="file to store result of --readUserEvent", default='')
parser.add_argument('--readIssueStatusFile', help="file to read a stored --readIssueStatus step from (for... some reason?)", default='')
parser.add_argument('--writeIssueStatusFile', help="file to store result of --readIssueStatus", default='')
parser.add_argument('-u','--githubUser', help="github user name", default='kuhnchris')
parser.add_argument('-v','--verbose', help="shows additional info, not good for parsing...", action="store_true",default='False')


def read_github_via_graphql(ep, cursor = ""):
    client = GraphQLClient(ep)
    clientVar = {}
    if cursor:
        clientVar = { "endCursor": cursor }

    client.inject_token("bearer "+TOKEN)

    """    result = client.execute('''
query ($endCursor: String){
  viewer {
    login
      issues(first: 10, after: $endCursor) {
      edges {
        node {
          title
          url
          closed
          closedAt
          createdAt
          updatedAt
          repository {
            name
            owner {
              login
            }
          }
          timeline(last: 10) {
            edges {
              node {
                ... on Commit {
                  author {
                    user {
                      id
                    }
                  }
                  message
                }
                ... on IssueComment {
                  author {
                    login
                  }
                  bodyText
                }
                ... on ClosedEvent {
                  actor {
                    login
                  }
                }
                ... on ReopenedEvent {
                  actor {
                    login
                  }
                }
              }
            }
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
    ''', clientVar)
"""
    mqQuery = '''
query ($endCursor: String){
  viewer {
    login
      issues(first: 10, after: $endCursor) {
      edges {
        node {
          title
          url
          number
          closed
          closedAt
          createdAt
          updatedAt
          repository {
            name
            owner {
              login
            }
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
'''
    result = client.execute(mqQuery, clientVar)
    f = json.loads(result)
    for obj in f["data"]["viewer"]["issues"]["edges"]:
        ctx = obj["node"]
        status = f"{colors.fg.red}open   X"
        if ctx["closed"]:
            status = f"{colors.fg.green}closed ✓"
        repo = f'{ctx["repository"]["owner"]["login"]}/{ctx["repository"]["name"]}'
        print(f"{status} | {repo.rjust(60)} | {ctx['title']} | {ctx['url']} | {ctx}{colors.reset}")

    pageCtx = f["data"]["viewer"]["issues"]["pageInfo"]
    if pageCtx['hasNextPage']:
        nextCursor = pageCtx['endCursor']
        # print(f"hasNextPage = YES, loading... $endCursor = {nextCursor}")
        read_github_via_graphql(ep,nextCursor)

    # print(result)


def readGithubUrlREST(url):
    jsonUrl = "https://api.github.com/users/kuhnchris/events"
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
                new_obj = {
                    "repository": obj["repo"]["name"],
                    "issue": obj["payload"]["issue"]["number"],
                    "title": obj["payload"]["issue"]["title"],
                    "url_api": obj["payload"]["issue"]["title"],
                    "url": f'https://www.github.com/{obj["repo"]["name"]}/issues/{obj["payload"]["issue"]["number"]}'
                }

    print(f'DEBUG: {jsonRet}')
    expDate = time.ctime(int(ret.headers["X-RateLimit-Reset"]))
    print(f'DEBUG: {ret.headers["X-RateLimit-Remaining"]} of {ret.headers["X-RateLimit-Limit"]} attempts remaining, expiring {expDate}')

    if next_link != "":
        readGithubUrl(next_link)


# readGithubUrl(jsonUrl)
# https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

read_github_via_graphql('https://api.github.com/graphql')
args = parser.parse_args()

# uncomment to see parameter(s)
print(args)
exit(1)
