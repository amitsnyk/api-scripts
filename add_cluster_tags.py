#An API script to tag all K8s clusters with the name of the cluster.

import requests

#Collect user input
org_id = input("Enter the org ID with the projects you would like to tag:")
auth_token = input("Enter your Snyk API token:")

#Populate parameters for API call to get all k8s projects
url = "https://snyk.io/api/v1/org/"+ org_id + "/projects"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token '+auth_token
}
values = """
  {
    "filters": {
      "origin": "kubernetes"
    }
  }
"""

#Send API call
response = requests.request("POST", url, headers=headers, data=values)

response_dict = response.json()

#Iterate through projects and assign tags based on cluster name
while response_dict['projects']:
    project = response_dict['projects'].pop()
    proj_id = project['id']
    cluster_name = project['imageCluster'].replace(" ","-")

    #Confirm the project does not already have a cluster tag
    if project['tags'] and "cluster" in project['tags'][0].values():
        print(proj_id+" has a cluster tag")
        #print(project["tags"])
        continue

    #Populate parameters for API call to add tags
    url = url = "https://snyk.io/api/v1/org/"+ org_id + "/project/"+proj_id+"/tags"
    values = f"""
      {{
        "key": "cluster",
        "value": "{cluster_name}"
      }}
    """
    #Print updates
    req = requests.request("POST", url, headers=headers, data=values)
    print("Updated "+proj_id+" with cluster tag: "+cluster_name)