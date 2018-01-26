import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Problem

def create_problem(problem_text, days):
    """
    Creates a problem with the given `problem_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Problem.objects.create(problem_text=problem_text, pub_date=time)

class ProblemViewTests(TestCase):
    def test_index_view_with_no_problems(self):
        """
        if no problem exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('interview_questions:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "У матросов нет вопросов.")
        self.assertQuerysetEqual(response.context['latest_problem_list'], [])

    def test_index_view_with_a_past_problem(self):
        """
        Problems with a pub_date in the past should be displayed on the
        index page.
        """
        create_problem(problem_text="Past problem.", days=-30)
        response = self.client.get(reverse('interview_questions:index'))
        self.assertQuerysetEqual(
            response.context['latest_problem_list'],
            ['<Problem: Past problem.>']
        )

    def test_index_view_with_a_future_problem(self):
        """
        Problems with a pub_date in the future should not be displayed on
        the index page.
        """
        create_problem(problem_text="Future problem.", days=30)
        response = self.client.get(reverse('interview_questions:index'))
        self.assertContains(response, "У матросов нет вопросов.")
        self.assertQuerysetEqual(response.context['latest_problem_list'], [])

    def test_index_view_with_future_problem_and_past_problem(self):
        """
        Even if both past and future problems exist, only past problems
        should be displayed.
        """
        create_problem(problem_text='Past problem.', days=-30)
        create_problem(problem_text='Future problem.', days=30)
        response = self.client.get(reverse('interview_questions:index'))
        self.assertQuerysetEqual(
            response.context['latest_problem_list'],
            ['<Problem: Past problem.>']
        )

    def test_index_view_with_two_past_problem(self):
        """
        The problems index page may display multiple problems.
        """
        create_problem(problem_text="Past problem 1.", days=-30)
        create_problem(problem_text="Past problem 2.", days=-5)
        response = self.client.get(reverse('interview_questions:index'))
        self.assertQuerysetEqual(
            response.context['latest_problem_list'],
            ['<Problem: Past problem 2.>', '<Problem: Past problem 1.>']
        )

    class ProblemIndexDetailTests(TestCase):
        def test_detail_view_with_a_future_problem(self):
            """
            The detail view of a problem with a pub_date in the future should
            return a 404 not found.
            """
            future_problem = create_problem(problem_text='Future question.', days=5)
            url = reverse('interview_questions:detail', args=(future_problem.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_detail_view_with_a_past_problem(self):
            """
            The detail view of a problem with a pub_date in the past should
            display the problem's text.
            """
            past_problem = create_problem(problem_text='Past problem.', days=-5)
            url = reverse('interview_questions:detail', args=(past_problem.id,))
            response = self.client.get(url)
            self.assertContains(response, past_problem.problem_text)

class ProblemMethodTests(TestCase):

    def test_was_published_recently_with_future_problem(self):
        """
        was_published_recently() should return False for problems whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_problem = Problem(pub_date=time)
        self.assertEqual(future_problem.was_published_recently(), False)

    def test_was_published_recently_with_old_problem(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_problem = Problem(pub_date=time)
        self.assertEqual(old_problem.was_published_recently(), False)

    def test_was_published_recently_with_recent_problem(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Problem(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)