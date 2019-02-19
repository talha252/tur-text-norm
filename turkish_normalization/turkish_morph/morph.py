import subprocess
from subprocess import DEVNULL, PIPE
from pathlib import Path


TOOL_DIR = Path(__file__).with_name("tr-morph")

def morph_base(in_text):
    """ Analyze the text using modified Kemal Oflazer's FST"""
    args = "./lookup -f lm_tfeatures.scr -utf8".split()
    data = "\n".join(in_text)
    p = subprocess.run(args, cwd=TOOL_DIR, input=data, stdout=PIPE, stderr=DEVNULL, encoding="UTF8")
    return p.stdout

def morphological_analyzer(words, validate_only=False, hard_validate=True):
    ret = morph_base(words).split('\n')
    results = []
    intermediate = []
    skip = False 
    for line in ret[:-1]:
        if not line:
            skip = False
            if not validate_only:
                results.append(intermediate)
                intermediate = []
            continue

        if not skip:           
            ret = line.split('\t')
            # sometimes fst return with only two tab character
            # for those situations use the except part
            if len(ret) == 3:
                surface, stem, pos = ret
            else:
                surface, pos = ret
                stem = ""

            if validate_only: 
                skip = True
                if pos != "*UNKNOWN*":
                    results.append(True)
                elif hard_validate:
                    results.append(False)
                elif "'" in surface or surface[0].isupper():
                    results.append("SOFT")
                else:
                    results.append(False)

            else:
                if pos != "*UNKNOWN*":
                    intermediate.append(stem + pos)
    return results





