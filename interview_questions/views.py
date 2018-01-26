# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from .models import Problem, Comment, Reply, Votes, Topic
from .forms import ProblemForm, CommentForm, ReplyForm

# main view

class IndexView(View):
    template_name = 'interview_questions/index.html'

    def get(self, request):
        problem_list = Problem.objects.all().order_by('-pub_date')
        title = 'Последние добавленные'
        ordering = request.GET.get('order')

        top_topics = Problem.objects.values('topic').annotate(amount=Count('topic')).order_by('-amount')
        names = {elem['screenname']: elem['name'] for elem in Topic.objects.values('name', 'screenname')}
        tt = [{'url': elem['topic'], 'amount': elem['amount'], 'topic': names.get(elem['topic'])} for elem in top_topics]

        now = timezone.now()
        if ordering == 'votes':
            problem_list = problem_list.order_by('-total_votes')
            title = 'Лучшие за все время'
        elif ordering == 'votes_day':
            delta = datetime.timedelta(days=1)
            title = 'Лучшие за сутки'
        elif ordering == 'votes_week':
            delta = datetime.timedelta(days=7)
            title = 'Лучшие за неделю'
        elif ordering == 'votes_month':
            delta = datetime.timedelta(days=30)
            title = 'Лучшие за месяц'

        if ordering in ['votes_day', 'votes_week', 'votes_month']:
            problem_list_ids = [item.id for item in problem_list if now - delta <= item.pub_date <= now]
            problem_list = Problem.objects.filter(id__in=problem_list_ids).order_by('-total_votes')

        paginator = Paginator(problem_list, 5)

        page = request.GET.get('page')
        try:
            problems = paginator.page(page)
        except PageNotAnInteger:
            problems = paginator.page(1)
        except EmptyPage:
            problems = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'problems': problems, 'title': title, 'top': tt})

class TopicView(View):
    template_name = 'interview_questions/index.html'

    def get(self, request, tp):
        problem_list = Problem.objects.filter(topic=tp).order_by('-pub_date')
        title = 'Последние добавленные по теме ' + tp
        ordering = request.GET.get('order')

        top_topics = Problem.objects.values('topic').annotate(amount=Count('topic')).order_by('-amount')
        names = {elem['screenname']: elem['name'] for elem in Topic.objects.values('name', 'screenname')}
        tt = [{'url': elem['topic'], 'amount': elem['amount'], 'topic': names.get(elem['topic'])} for elem in
              top_topics]

        now = timezone.now()
        if ordering == 'votes':
            problem_list = problem_list.order_by('-total_votes')
            title = 'Лучшие за все время'
        elif ordering == 'votes_day':
            delta = datetime.timedelta(days=1)
            title = 'Лучшие за сутки'
        elif ordering == 'votes_week':
            delta = datetime.timedelta(days=7)
            title = 'Лучшие за неделю'
        elif ordering == 'votes_month':
            delta = datetime.timedelta(days=30)
            title = 'Лучшие за месяц'

        if ordering in ['votes_day', 'votes_week', 'votes_month']:
            problem_list_ids = [item.id for item in problem_list if now - delta <= item.pub_date <= now]
            problem_list = Problem.objects.filter(id__in=problem_list_ids).order_by('-total_votes')

        paginator = Paginator(problem_list, 5)

        page = request.GET.get('page')
        try:
            problems = paginator.page(page)
        except PageNotAnInteger:
            problems = paginator.page(1)
        except EmptyPage:
            problems = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'problems': problems, 'title': title, 'top': tt})
# add post

class AddView(View):
    template_name = 'interview_questions/add.html'
    form_class = ProblemForm
    success_url = '/'

    # display blank form
    def get(self, request):
        if request.user.is_authenticated():
            form = self.form_class(None)
            title = "Добавить вопрос/задачу"
            return render(request, self.template_name, {'title': title, 'form': form, 'user': request.user})
        else:
            messages.add_message(request, messages.ERROR, 'Войдите или зарегистрируйтесь.')
            return redirect('interview_questions:index')

    # process data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and request.user.is_authenticated():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.user = request.user
            post.save()
            return redirect('interview_questions:index')

        return render(request, self.template_name, {'form': form, 'user': request.user})

# view of the page of post

class DetailView(View):

    template_name = 'interview_questions/detail.html'
    form_class = CommentForm

    def get(self, request, pk):
        problem = Problem.objects.get(id=pk)
        comment_list = problem.comment_set.all().order_by('-total_votes')
        paginator = Paginator(comment_list, 5)

        page = request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        if request.user.is_authenticated():
            have_comments = Comment.objects.filter(user=request.user, problem=problem).count() > 0
        else:
            have_comments = False

        other_problems = Problem.objects.filter(topic=problem.topic).exclude(id=problem.id)
        if request.user.is_authenticated():
            form = self.form_class(None)
            reply_form = ReplyForm(None)
            return render(request, self.template_name, {'form': form, 'reply_form': reply_form,
                                                        'problem': problem, 'user': request.user,
                                                        'have_comments': have_comments,
                                                        'comments': comments,
                                                        'other_problems': other_problems})

        return render(request, self.template_name, {'problem': problem, 'user': request.user,
                                                    'have_comments': have_comments,
                                                    'comments': comments, 'other_problems': other_problems})

class EditView(View):
    template_name = 'interview_questions/add.html'
    form_class = ProblemForm

    def get(self, request, pk):

        if request.user.is_authenticated():
            problem = Problem.objects.get(id=pk)

            if request.user.is_authenticated():
                have_comments = Comment.objects.filter(user=request.user, problem=problem).count() > 0
            else:
                have_comments = False

            if request.user == problem.user:
                form = self.form_class(instance=problem)
                title = 'Редактировать условия задачи/вопроса'
                return render(request, self.template_name, {'title': title, 'form': form, 'problem': problem,
                                                            'user': request.user, 'have_comments': have_comments})
        return redirect('interview_questions:detail', pk=pk)

    def post(self, request, pk):
        form = self.form_class(request.POST)

        problem = Problem.objects.get(id=pk)
        if form.is_valid() and request.user.is_authenticated() and request.user == problem.user:
            new_post = form.save(commit=False)
            post = Problem.objects.get(id=pk)
            post.problem_text = new_post.problem_text
            post.topic = new_post.topic
            post.position = new_post.position
            post.wiki_answer = new_post.wiki_answer
            post.pub_date = timezone.now()
            post.user = request.user
            post.save()

            return redirect('interview_questions:detail', pk=pk)

        return render(request, self.template_name, {'form': form, 'user': request.user})

class DeleteView(View):
    template_name = 'interview_questions/index.html'

    def get(self, request, pk):
        problem = Problem.objects.get(id=pk)

        if request.user.is_authenticated() and request.user == problem.user:
            problem.delete()
            messages.add_message(request, messages.SUCCESS, 'Запись успешно удалена.')
            return redirect('interview_questions:index')

        return redirect('interview_questions:index')

class VoteView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        pk = request.POST['id']
        val = int(request.POST['vote'])
        obj = request.POST['obj']
        print(request.POST)
        if obj == 'problem':
            problem = Problem.objects.get(id=pk)
            objct = problem
        elif obj == 'comment':
            comment = Comment.objects.get(id=pk)
            problem = comment.problem
            objct = comment
        elif obj == 'reply':
            reply = Reply.objects.get(id=pk)
            comment = reply.comment
            problem = comment.problem
            objct = reply

        if request.user.is_authenticated():
            if not Votes.objects.filter(obj=obj, obj_id=pk, user=request.user).exists():
                vote = Votes.objects.create(
                    value=val,
                    user=request.user,
                    obj=obj,
                    obj_id=pk
                )
            else:
                vote = Votes.objects.get(obj=obj, obj_id=pk, user=request.user)
                if vote.value == val:
                    vote.value = 0
                else:
                    vote.value = val
            vote.save()

            objct.total_votes = Votes.objects.filter(obj=obj, obj_id=pk, value=1).count() - \
                                Votes.objects.filter(obj=obj, obj_id=pk, value=-1).count()
            objct.save()
            return redirect('interview_questions:detail', pk=problem.id)
        return redirect('interview_questions:detail', pk=problem.id)

# comment views

class AddCommentView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        text = request.POST['text']
        pk = request.POST['pk']
        problem = Problem.objects.get(id=pk)
        if request.user.is_authenticated():
            have_comments = Comment.objects.filter(user=request.user, problem=problem).count() > 0
        else:
            have_comments = False

        if text != "" and request.user.is_authenticated():
            comment = Comment.objects.create(
                text = text,
                pub_date = timezone.now(),
                user = request.user,
                problem = problem)
            comment.save()
            return redirect('interview_questions:detail', pk=pk)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'problem': problem,
                                                    'pk': pk, 'user': request.user,
                                                    'have_comments': have_comments})

class EditCommentView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):

        text = request.POST['text']
        comment_id = request.POST['comment_id']
        comment = Comment.objects.get(id=comment_id)
        problem = comment.problem
        pk = problem.id

        if request.user.is_authenticated() and request.user == comment.user:
            comment.text = text
            comment.pub_date = timezone.now()
            comment.user = request.user
            comment.problem = problem
            comment.save()
            return redirect('interview_questions:detail', pk=pk)

        return render(request, self.template_name, {'problem': problem, 'user': request.user})

class DeleteCommentView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        comment_id = request.POST['comment_id']
        comment = Comment.objects.get(id=comment_id)
        problem = comment.problem
        if request.user.is_authenticated() and request.user == comment.user:
            comment.delete()
            return redirect('interview_questions:detail', pk=problem.id)
        return redirect('interview_questions:detail', pk=problem.id)

class VoteCommentView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        comment_id = request.POST['comment_id']
        votes = int(request.POST['vote'])
        comment = Comment.objects.get(id=comment_id)
        problem = comment.problem

        if request.user.is_authenticated():
            comment.votes = votes
            comment.save()
            return redirect('interview_questions:detail', pk=problem.id)

        return redirect('interview_questions:detail', pk=problem.id)

# replies for comment

class ReplyView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        text = request.POST['text']
        comment_id = request.POST['comment_id']
        comment = Comment.objects.get(id=comment_id)
        problem = comment.problem
        if text != "" and request.user.is_authenticated():
            reply = Reply.objects.create(
                text=text,
                pub_date=timezone.now(),
                user=request.user,
                comment=comment)
            reply.save()
            return redirect('interview_questions:detail', pk=problem.id)


        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'problem': problem,
                                                        'user': request.user})

class EditReplyView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        text = request.POST['text']
        reply_id = request.POST['reply_id']
        reply = Reply.objects.get(id=reply_id)
        comment = reply.comment
        problem = comment.problem

        if request.user.is_authenticated() and request.user == reply.user:
            reply.text = text
            reply.pub_date = timezone.now()
            reply.user = request.user
            reply.save()
            return redirect('interview_questions:detail', pk=problem.id)

        return render(request, self.template_name, {'user': request.user})

class DeleteReplyView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        reply_id = request.POST['reply_id']
        reply = Reply.objects.get(id=reply_id)
        comment = reply.comment
        problem = comment.problem
        if request.user.is_authenticated() and request.user == reply.user:
            reply.delete()
            return redirect('interview_questions:detail', pk=problem.id)
        return redirect('interview_questions:detail', pk=problem.id)

class VoteReplyView(View):
    template_name = 'interview_questions/detail.html'

    def post(self, request):
        reply_id = request.POST['reply_id']
        reply = Reply.objects.get(id=reply_id)
        votes = int(request.POST['vote'])
        comment = reply.comment
        problem = comment.problem

        if request.user.is_authenticated():
            reply.votes = votes
            reply.save()
            return redirect('interview_questions:detail', pk=problem.id)

        return redirect('interview_questions:detail', pk=problem.id)