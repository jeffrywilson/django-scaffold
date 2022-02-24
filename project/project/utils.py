from git import Repo
from project.settings import settings
import time

def git_info_status():
    
    """Get metadata branch to show at the top of the app.
        This functions helps to see what the last modification and others info about 
        the last commit in the environment
    """
    try:
        if settings.DEBUG: # No production environment (dev, staging)
            repo = Repo(settings.REPO_DIR) # The repo search for project root where is .git files
            headcommit = repo.head.commit
            commit_info = "Branch: " + str(repo.active_branch) + " | Hash resume: " + str(headcommit.hexsha[0:7]) + '... | Date: ' +  time.strftime("%a, %d %b %Y %H:%M", time.localtime(headcommit.committed_date)) + " | Committer: " + str(headcommit.committer.name) +" | Commit msg: "+ str(headcommit.message) 
        else: commit_info = None
    except:
        commit_info = None
    return commit_info 

def git_commit_history():
    """
    Return the last 10 Commits info for the branch in readable format
    """
    try:
        repo = Repo(settings.REPO_DIR) # The repo search for project root where is .git files
        headcommit = repo.head.commit
        commits = list(repo.iter_commits(str(repo.active_branch), max_count=10))
    except:
        commits = None
    return commits