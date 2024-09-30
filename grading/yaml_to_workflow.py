import yaml
import os
import argparse

SETUP_COMMAND = "sudo -H pip install --quiet pytest pandas pyyaml"
ANSWER_URL = "https://github.com/mwklose/F2024-answer-keys/raw/main/"

TYPE_DICT = {
    "exact": "grading/test_exact_output.py", 
    "decimal": "grading/test_decimal_places.py", 
    "readme": "grading/test_readme.py"
}

def yaml_to_workflow(filepath: str, outpath: str): 
    fp: str = os.path.expanduser(path=filepath)
    if not os.path.exists(path=filepath): 
        raise Exception(f"[yaml_to_workflow] Unable to find file {filepath}")

    with open(file=fp, mode="r") as f: 
        y = yaml.safe_load(stream=f)

    # Holds Dict for final yaml
    yaml_dict = {}

    # Parsing y
    if "assignment" not in y: 
        raise Exception(f"[yaml_to_workflow] Assignment name not defined in yaml file")

    yaml_dict["name"] = f"{y['assignment']} Autograding Tests"
    yaml_dict["on"] = ["push"]
    yaml_dict["permissions"] = {"checks": "write", "actions": "read", "contents": "read"}

    
    steps = []
    steps.append({"name": "Checkout code", "uses": "actions/checkout@v4"})
    
    if "tests" not in y: 
        raise Exception(f"[yaml_to_workflow] Tests not defined in yaml file")

    if not isinstance(y["tests"], list): 
        raise Exception(f"[yaml_to_workflow] Tests should be defined as a list of files")

    needed_keys = ["name", "points", "command"]
    
    test_names = []
    report_env = {}
    for test in y["tests"]: 
        newtest = {}
        if not isinstance(test, dict): 
            raise Exception(f"[yaml_to_workflow] Each test should be a dictionary")

        for k in needed_keys: 
            if k not in test: 
                raise Exception(f"[yaml_to_workflow] Test {test} missing {k}")


        newtest["name"] = test["name"]
        newtest["id"] = "-".join(newtest["name"].lower().split(" "))
        test_names.append(newtest["id"])
        newtest["uses"] = "classroom-resources/autograding-command-grader@v1"

        newtest["with"] = {
            "test-name": test["name"], 
            "setup-command": SETUP_COMMAND,
            "command": f"{test["command"]} --no-header -rfs", 
            "timeout": 10, 
            "max-score": test["points"]
        }

        steps.append(newtest)

        report_env[f"{newtest["name"].upper()}_RESULTS"] = f"${{{{ steps.{newtest["name"].lower()}.outputs.result }}}}"

    reporter = {
        "name": "Autograding Reporter", 
        "uses": "classroom-resources/autograding-grading-reporter@v1", 
        "env": report_env, 
        "with": {"runners": f"{','.join(test_names)}"}}

    steps.append(reporter)

    # Finish setting up yaml_dict
    yaml_dict["jobs"] = {"run-autograding-tests": {
        "runs-on": "ubuntu-latest", 
        "if": "github.actor != 'github-classroom[bot]'", 
        "steps": steps
    }}

    # Write results to file
    os.makedirs(name=os.path.split(outpath)[0], exist_ok=True)
    with open(file=outpath, mode="w") as f: 
        yaml.dump(data=yaml_dict, stream=f, sort_keys=False)

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(prog="Create workflow from YAML.")
    parser.add_argument("yaml_file", type=str)
    args: argparse.Namespace = parser.parse_args()

    yaml_to_workflow(filepath=args.yaml_file, outpath=".github/workflows/classroom.yml")