import os
from os.path import splitext, join
import subprocess
import shutil

from github3 import login

gh = login(token=os.environ.get("GITHUB_API_TOKEN"))
NOTEBOOK_DIR = 'notebooks'
REF = 'master'


def get_listing():
    repos = []
    # Find all repos having a notebook subdirectory.
    for repo in gh.iter_repos():
        content = repo.contents('', ref=REF)
        if content and NOTEBOOK_DIR in content:
            repos.append(repo)

    listing = {}
    for repo in repos:
        notebooks = repo.contents(NOTEBOOK_DIR, ref=REF)
        names = [splitext(nb) for nb in notebooks.keys()]
        listing[repo.name] = sorted([name for name, ext in names
                                     if ext == '.html'])

    return listing


def get_content(repo_name, filename):
    repo = gh.repository(gh.user().login, repo_name)
    filename = filename + ".html"
    notebook = repo.contents(join(NOTEBOOK_DIR, filename), ref=REF)
    if notebook.size > 1000000:
        content = get_from_clone(repo, filename, REF)
    else:
        content = notebook.decoded
    return content


def get_from_clone(repo, filename, ref=None):
    output_dir = "/tmp/{}".format(repo.name)
    clone(repo, output_dir, ref)
    f = open("/tmp/{}/{}/{}".format(repo.name, NOTEBOOK_DIR, filename))
    content = f.read()
    # Remove target directory.
    shutil.rmtree(output_dir)
    return content


def clone(repo, output_dir, ref=None):
    token = os.environ.get("GITHUB_API_TOKEN")
    url = "https://{}:@github.com/{}/{}".format(
        token, repo.owner.login, repo.name)
    args = ["/usr/bin/git", "clone", url, output_dir]
    if ref:
        args.append("--branch")
        args.append(ref)

    subprocess.call(args)
