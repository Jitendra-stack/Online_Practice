from django.urls import path
from solveproblems.views import problems_list,problem_detail, add_problem, add_test_case

urlpatterns = [
    path("all/", problems_list, name="problems-list"),
    path("all/<int:problem_id>/", problem_detail, name="problem_detail"),
    path("add/", add_problem, name="add_problem"),
    path("testcase/add/<int:problem_id>/", add_test_case, name="add_test_case")
]
