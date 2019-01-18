import os
import sys
import yaml
import unittest
import requests

def print_usage(argv):
    print("Usage:")
    print(" ".join(argv) + " my_sites_to_check.yaml")
    exit(1)


class WebSiteHealthChecks(unittest.TestCase):

    def test_can_reach_google(self):
        elk_url = sites['GOOGLE']
        resp = requests.get(elk_url)
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage(sys.argv)
    else:
        with open(sys.argv[1]) as fh:
            sites = yaml.safe_load(fh)

    suite = unittest.TestLoader().loadTestsFromTestCase(WebSiteHealthChecks)
    unittest.TextTestRunner(verbosity=2).run(suite)
