from django.shortcuts import render
from project.utils import git_info_status, git_commit_history
from django.views.generic import TemplateView
# Create your views here.
class LandingView(TemplateView):
    template_name = "landing/index.html"
    
    def get(self, request):
        git_info = git_info_status()
        if git_info != None: 
            request.session['git_info'] = git_info 
        return render(request, self.template_name)

class VersionView(TemplateView):
    template_name = "landing/version.html"

    def get_context_data(self, **kwargs):
        #call the base of the implementation first to get a context
        context = super().get_context_data(**kwargs)
        commits = git_commit_history()
        if commits:
            context['repo_name'] = str(commits[0].repo.active_branch)
            context['commits'] =  commits
        return context
    