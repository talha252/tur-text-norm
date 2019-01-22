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

def morphological_analyzer(words, validate_only=False):
    ret = morph_base(words).split('\n')
    results = []
    intermediate = []
    skip = False 
    for line in ret[:-1]:
        if not line:
            skip = False
            if not validate_only and intermediate:
                results.append(intermediate)
                intermediate = []
            continue

        if not skip:
            try:
                _ , stem, pos = line.split('\t')
            # sometimes fst return with only two tab character
            # for those situations use the except part
            except ValueError:
                _, pos = line.split('\t')
                stem = ""

            if validate_only: 
                skip = True
                results.append(pos != "*UNKNOWN*")
            else:
                if pos != "*UNKNOWN*":
                    intermediate.append(stem + pos)
                else:
                    results.append(None)
                
    
    return results





