import os
import re


def test_regex(regex, files: str): 
    filelist = files.replace("[", "").replace("]", "").split(",")
    for f in filelist: 
        assert os.path.exists(f), f"File {f} does not exist; check its location."
        with open(f, "r") as fp: 
            your_code = fp.read()

        assert re.search(regex, your_code, re.IGNORECASE) is not None, f"Try again; unable to match pattern {regex}"

            
    