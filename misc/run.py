import requests

def run_query(query, variables):
    request = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 404:
        print ("Invalid search.")
        return
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))