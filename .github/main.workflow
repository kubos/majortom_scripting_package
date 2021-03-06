workflow "Publish" {
  on = "push"
  resolves = ["publish-to-pypi"]
}

action "publish-to-pypi" {
  needs = "Master"
  uses = "mariamrf/py-package-publish-action@master"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  env = {
    BRANCH = "master"
    PYTHON_VERSION = "3.7.0"
  }
}

# Filter for master branch
action "Master" {
  uses = "actions/bin/filter@master"
  args = "branch master"
}
