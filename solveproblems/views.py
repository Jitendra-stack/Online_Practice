from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission, TestCase
from django.contrib import messages

# List all problems
def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problems/problem_list.html', {'problems': problems})

# View problem details and submissions
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    user = request.user if request.user.is_authenticated else None

    submissions = Submission.objects.filter(user=user, problem=problem) if user else None

    context = {
        'problem': problem,
        'submissions': submissions if submissions else [],
        'code_value': submissions.first().code_value if submissions and submissions.exists() else "",
        'is_authenticated': request.user.is_authenticated
    }

    return render(request, 'problems/problem_detail.html', context)

# Add a new problem
@login_required
def add_problem(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title and description:
            Problem.objects.create(title=title, description=description)
            messages.success(request, "Problem added successfully!")
            return redirect('problem_list')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'problems/add_problem.html')

# Add test cases for a problem
@login_required
def add_testcase(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)

    if request.method == 'POST':
        input_data = request.POST.get('input_data', '').strip()
        expected_output = request.POST.get('expected_output', '').strip()

        if input_data and expected_output:
            TestCase.objects.create(problem=problem, input_data=input_data, expected_output=expected_output)
            messages.success(request, "Test case added successfully!")
            return redirect('problem_detail', problem_id=problem.id)
        else:
            messages.error(request, "Both input and expected output are required.")

    return render(request, 'problems/add_testcase.html', {'problem': problem})
