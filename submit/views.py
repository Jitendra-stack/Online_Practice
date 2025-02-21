from django.shortcuts import render
from submit.forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path


def submit(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            print("Language Submitted:", submission.language)
            print("Code Submitted:\n", submission.code)

            output = run_code(
                submission.language, submission.code, submission.input_data
            )

            print("Execution Output:\n", output)
            submission.output_data = output
            submission.save()
            form = CodeSubmissionForm(instance=submission)

            return render(request, "index.html", {"form": form, "output": output})
    else:
        form = CodeSubmissionForm()

    return render(request, "index.html", {"form": form})


def run_code(language, code, input_data):
    try:
        project_path = Path(settings.BASE_DIR)
        directories = ["codes", "inputs", "outputs"]

        for directory in directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)

        codes_dir = project_path / "codes"
        inputs_dir = project_path / "inputs"
        outputs_dir = project_path / "outputs"

        unique = str(uuid.uuid4())
        code_file_name = f"{unique}.{language}"
        input_file_name = f"{unique}.txt"
        output_file_name = f"{unique}.txt"

        code_file_path = codes_dir / code_file_name
        input_file_path = inputs_dir / input_file_name
        output_file_path = outputs_dir / output_file_name

        # Save code and input
        with open(code_file_path, "w") as code_file:
            code_file.write(code)
        with open(input_file_path, "w") as input_file:
            input_file.write(input_data)

        # Ensure the output file exists
        output_file_path.touch()

        if language in ["cpp", "c"]:
            executable_path = codes_dir / f"{unique}.exe"

            compiler = "g++" if language == "cpp" else "gcc"
            print(f"Compiling {language.upper()} Code...")
            compile_result = subprocess.run(
                [compiler, str(code_file_path), "-o", str(executable_path), "-static"],
                capture_output=True,
                text=True
            )

            print("Compile Result:", compile_result.returncode)
            print("Compile Error Output:", compile_result.stderr)

            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"

            if not executable_path.exists():
                return "Error: Executable file not created."

            print(f"Running {language.upper()} Executable...")
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                execution_result = subprocess.run(
                    [str(executable_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5  
                )

                print("Execution Result:", execution_result.returncode)
                print("Runtime Error Output:", execution_result.stderr)

                if execution_result.returncode != 0:
                    return f"Runtime Error:\n{execution_result.stderr}"

        elif language == "py":
            print("Running Python Code...")
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                execution_result = subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )

                print("Execution Result:", execution_result.returncode)
                print("Runtime Error Output:", execution_result.stderr)

                if execution_result.returncode != 0:
                    return f"Runtime Error:\n{execution_result.stderr}"

        # Read and return output
        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()

        return output_data.strip()

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."

    except Exception as e:
        return f"Unexpected Error: {str(e)}"
