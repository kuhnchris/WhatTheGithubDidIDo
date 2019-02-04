import json
from graphqlclient import GraphQLClient
from config import TOKEN


# Python program to print
# colored text and background
class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


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

myIssues = []

def read_github_via_graphql(ep, arr=[], cursor=""):
    client = GraphQLClient(ep)
    clientVar = {}
    if cursor:
        clientVar = {"endCursor": cursor}

    client.inject_token("bearer " + TOKEN)

    result = client.execute(mqQuery, clientVar)
    f = json.loads(result)
    for obj in f["data"]["viewer"]["issues"]["edges"]:
        arr.append(obj['node'])

    page_ctx = f["data"]["viewer"]["issues"]["pageInfo"]
    if page_ctx['hasNextPage']:
        next_cursor = page_ctx['endCursor']
        read_github_via_graphql(ep, arr, next_cursor)


def printMyIssues(arr):
    maxLenRep = 0
    maxLenUrl = 0
    # figure out max length
    for obj in arr:
        repo = f'{obj["repository"]["owner"]["login"]}/{obj["repository"]["name"]}'
        if len(obj['url']) > maxLenUrl:
            maxLenUrl = len(obj['url'])
        if len(repo) > maxLenRep:
            maxLenRep = len(repo)

    for obj in arr:
        ctx = obj
        status = f"{colors.fg.red}open   X"
        if ctx["closed"]:
            status = f"{colors.fg.green}closed ✓"
        repo = f'{ctx["repository"]["owner"]["login"]}/{ctx["repository"]["name"]}'
        print(f"{status} | {repo.rjust(maxLenRep)} | {str(ctx['number']).rjust(5)} | {ctx['url'].ljust(maxLenUrl)} | {ctx['title']}{colors.reset}")


read_github_via_graphql('https://api.github.com/graphql', myIssues)
printMyIssues(myIssues)
