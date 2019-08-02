#!/usr/bin/env python
import json
import yaml
import sys

jsonData = json.load(sys.stdin)
yaml.safe_dump(jsonData, sys.stdout, allow_unicode=True)
