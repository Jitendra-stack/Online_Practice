import json
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .forms import ProblemForm, TestCaseForm
from django.views.decorators.csrf import csrf_exempt
from .models import Problem, Submission
from submit.views import run_code
from accounts.models import Users
# Create your views here.

def problems_list(request):
    problems = Problem.objects.all()
    
    context = {
        'problems':problems,
    }
    template = loader.get_template('all_problems.html')
   
    return HttpResponse(template.render(context,request))



def submission_setter(sub):
        if  sub.verdict == "AC":
            verdict = "Accepted"
        else:
            verdict = "Wrong Answer"      
        if sub.language=="py":
           language ="Python"
        elif sub.language=="c":
            language = "C"
        else:
            language = "C++"
        return {"language": language,
                    "verdict": verdict}

def problem_detail(request, problem_id):
    
    problem = Problem.objects.get(id=problem_id)
    test_cases = problem.test_cases.all()
    user = get_object_or_404(Users, username=request.user.username) if request.user.is_authenticated else None
    
    test = []
    for i in test_cases:
        test.append({"input":i.input,
                     "output":i.output,
                     "result": None})

    if request.method == 'POST':
        # Capture the user's submitted code
        selected_language = request.POST.get('language')
        code_value = request.POST.get('code')
               
        # Here you can pass the `user_code` to a function for processing
        all_pass = True
        for test_case in test:
         
         output = run_code(selected_language, code_value, test_case["input"]) # Assume you have a function `run_code` to process the code
         temp_bool = output == test_case["output"]
         if not temp_bool:
             all_pass = False
         
         test_case["result"] = temp_bool

        if 'submit_code' in request.POST:
            if request.user.is_authenticated:
                Submission.objects.create(
                    user= user,
                    problem=problem,
                    code=code_value,
                    language=selected_language,
                    verdict= "AC"  if all_pass else "WA",
                )
    else:
        # Default values for GET request (first load of the page)
        selected_language = None
        code_value = ""
    # Retrieve all submissions for the current user and problem
    submissions = Submission.objects.filter(user=user, problem=problem)
    context_sub = []
    for sub in submissions:
        context_sub.append(submission_setter(sub))
    print(context_sub)
    
    context = {
        'problem': problem,
        'selected_language': selected_language,
        'code_value': code_value,
        'test_cases': test,
        'submissions': context_sub,
        'is_authenticated': user
    }
    template = loader.get_template('problem_detail.html')
    return HttpResponse(template.render(context,request))



@csrf_exempt
def add_problem(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from the request body
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format.'
            }, status=400)

        form = ProblemForm(data)  # Pass the parsed JSON data to the form
        if form.is_valid():
            problem = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Problem added successfully!',
                'problem': {
                    'title': problem.title,
                    'description': problem.description,
                    'difficulty': problem.difficulty,
                    'tag': problem.tag
                }
            }, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed.'
        }, status=405)
 
@csrf_exempt
def add_test_case(request, problem_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from the request body
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format.'
            }, status=400)

        # Get the problem by ID
        problem = get_object_or_404(Problem, id=problem_id)

        # Add the problem instance to the data dictionary
        data['problem'] = problem.id

        form = TestCaseForm(data)  # Pass the parsed JSON data to the form
        if form.is_valid():
            test_case = form.save(commit=False)
            test_case.problem = problem  # Associate the test case with the problem
            test_case.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Test case added successfully!',
                'test_case': {
                    'input': test_case.input,
                    'output': test_case.output,
                    'problem_id': test_case.problem.id
                }
            }, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed.'
        }, status=405)