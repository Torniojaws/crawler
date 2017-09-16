"""This is used to generate the site rules/requirements."""
import os
import requests


class Rules():
    def get(self, source):
        if source[:4] == "http":
            result = self.remote_reqs(source)
        else:
            result = self.local_reqs(source)

        return result

    def remote_reqs(self, uri):
        """Retrieve requirements from a remote file"""
        resp = requests.get(uri)
        sr = resp.text.splitlines()

        return self.create_list(sr)

    def local_reqs(self, filename):
        """Retrieve requirements from a local file in the project root"""
        from apps.config.config import PROJECT_ROOT

        path = os.path.join(PROJECT_ROOT, filename)
        with open(path, "r") as file:
            sr = file.read().splitlines()

        return self.create_list(sr)

    def create_list(self, data):
        """Parse the data into a list of dicts, where key=site and value=requirement"""
        delimiter = data[0].strip("delimiter")

        site_requirements = []
        # Skip the first row, which is the delimiter definition
        for req in data[1:]:
            site, requirement = req.split(delimiter)
            site_dict = {}
            site_dict[site] = requirement
            site_requirements.append(site_dict)

        return site_requirements
