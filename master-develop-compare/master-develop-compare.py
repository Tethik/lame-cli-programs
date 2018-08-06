import fnmatch
import requests
import crayons
import click
import keyring

class GithubClient(object):
  def __init__(self, api_key):
    self.session = requests.Session()
    self.session.headers.update({"Authorization": f"Bearer {api_key}"})

  def list_repositories_matching(self, matchFilter=None):
    query = """
    {
      viewer {
        repositories(first: 100) {
          nodes {
            nameWithOwner
          }
        }
        organizations(first: 100) {
          nodes {
            name
            repositories(first: 100) {
              nodes {
                nameWithOwner
              }
            }
          }
        }
      }
    }
    """
    url = "https://api.github.com/graphql"
    resp = self.session.post(url, json={"query": query, "variables": []})
    resp = resp.json()
    names = [n["nameWithOwner"] for n in resp["data"]["viewer"]["repositories"]["nodes"]]

    for org in resp["data"]["viewer"]["organizations"]["nodes"]:
      names += [n["nameWithOwner"] for n in org["repositories"]["nodes"]]

    if matchFilter:
      return fnmatch.filter(names, matchFilter)
    return names


  def compare_master_develop(self, ownerWithName):
    try:
      url = f"https://api.github.com/repos/{ownerWithName}/compare/master...develop"

      resp = self.session.get(url)
      if resp.status_code == 404:
        return 0, None

      if resp.status_code != 200:
        print(url)
        print(resp)
        raise Exception(f"Failed to fetch comparison for {ownerWithName}. Ensure that oauth token has correct permissions.")

      resp = resp.json()
      return resp["ahead_by"], resp
    except KeyError:
      return 0, None


@click.command()
@click.argument('match_filter')
@click.option('--reset-token', default=False, is_flag=True, help="Flag to reset the github token stored in the keyring")
@click.option('--threshold', default=1, help="Threshold amount of commits to display the repo in the list.")
def main(match_filter, reset_token, threshold):
  """
  Compares develop and master branches for github repositories to detect where a new release is needed.

  MATCH_FILTER is a glob-like filter that decides which repositories should be included for the report. Repositories
  are listed by owner/name. E.g. wellnow-group/documentation. So to match on all wellnow-group repos, simply use
  the "wellnow*" pattern.
  """
  token = keyring.get_password('master-develop-compare', 'github')
  if not token or reset_token:
    token = click.prompt("Github OAuth Token").strip()
    keyring.set_password('master-develop-compare', 'github', token)

  client = GithubClient(token)
  repos = client.list_repositories_matching(match_filter)
  need_release = []
  visited = set()
  with click.progressbar(repos, label=f"Fetching {len(repos)} repos matching \"{match_filter}\"") as bar:
    for repo in bar:
      commits_ahead, info = client.compare_master_develop(repo)
      if commits_ahead >= threshold and repo not in visited:
        need_release.append((repo, commits_ahead, info))
        visited.add(repo)

  if not need_release:
    click.secho("All repositories are up to date!", color="green")
    return

  click.secho("The following repos are out of date:", color="blue")
  for repo, ahead_by, info in sorted(need_release, key=lambda x: -x[1]):
    click.echo(f"* {repo.ljust(50)} Commits Ahead: {ahead_by}")
    for commit in info["commits"]:
      commit_summary = commit["commit"]["message"].split("\n")[0]
      click.echo(f'\t{crayons.blue(commit["sha"][:16])} {commit_summary}')
    click.echo()


if __name__ == "__main__":
  main()



