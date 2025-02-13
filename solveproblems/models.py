from django.db import models
from accounts.models import Users

class Problem(models.Model):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'

    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    title = models.CharField(max_length=125)
    description = models.TextField()
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    tag = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class TestCase(models.Model):
    input = models.CharField(max_length=255)  # You can adjust max_length as needed
    output = models.CharField(max_length=255)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')

    def __str__(self):
        return f"TestCase for Problem: {self.problem.title}"


class Submission(models.Model):
    VERDICT_CHOICES = [
        ('AC', 'Accepted'),
        ('WA', 'Wrong Answer'),
        # Add more verdicts as needed
    ]

    user = models.ForeignKey(Users, related_name="submissions", on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="submissions", on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)
    verdict = models.CharField(max_length=3, choices=VERDICT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user} for Problem {self.problem.id} - {self.verdict}"
