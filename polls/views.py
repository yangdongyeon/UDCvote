from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, Vote
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def voting_error(request):
    return render(request, 'polls/error.html')


class IndexView(generic.ListView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class DetailView(generic.DetailView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = Question
    template_name = "polls/detail.html"
    def get(self, request, *args, **kwargs):
        # 객체를 가져옴 (여기서는 투표 안건)
        self.object = self.get_object()
        # 현재 사용자가 이 안건에 이미 투표했는지 확인
        if Vote.objects.filter(user=request.user, question=self.object).exists():
            # 이미 투표했다면 결과 페이지로 리디렉션
            return redirect('polls:results', pk=self.object.pk)
        # 투표하지 않았다면 정상적으로 상세 페이지를 렌더링
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ResultsView(generic.DetailView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    model = Question
    template_name = "polls/results.html"

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # 사용자가 이미 이 질문에 대해 투표했는지 확인
    if Vote.objects.filter(user=request.user, question=question).exists():
        messages.error(request, "You have already voted in this poll.")
        return redirect('polls:voting_error')

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with error message.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 투표 기록 생성
        Vote.objects.create(user=request.user, question=question)
        # HttpResponseRedirect로 리디렉션
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

