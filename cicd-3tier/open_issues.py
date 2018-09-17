#! /usr/bin/env python
"""This script stages Issues to GitLab based on a CSV fileself.
Copyright (c) 2018 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import the csv library
import csv
import sys
import requests

# Expects the following arguments incomingself.
#  - gitlab_host
#  - gitlab_token
#  - project_id
#  - user_id
#  - issues_file
# If not found, exit and error
if len(sys.argv) != 6:
    print("Error: Arguments not found.")
    print(" Command must be used in format of: ")
    print("    open_issues.py gitlab_host gitlab_token project_id user_id issues_file")
    print("   ")
    sys.exit()

# Get variables from arguments
gitlab_host = sys.argv[1]
gitlab_token = sys.argv[2]
project_id = sys.argv[3]
user_id = sys.argv[4]
issues_file = sys.argv[5]

# Setup variablees for request
url_base = "{}/api/v4".format(gitlab_host)
headers = {"PRIVATE-TOKEN": gitlab_token}
issues_url = "{base}/projects/{project_id}/issues".format(base=url_base, project_id=project_id)

opened_issues = []

# Open the issues file, and create new issues for each line
with open(issues_file) as f:
    csv_python = csv.reader(f)
    for row in csv_python:
        issue = {
            "title": row[0],
            "description": row[1],
            "assignee_ids": [user_id],
            "labels": row[2]
        }
        # print(issue)
        r = requests.post(issues_url, headers = headers, json = issue)
        opened_issues.append(r.json())
