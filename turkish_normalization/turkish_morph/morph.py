import subprocess
from subprocess import DEVNULL, PIPE
from pathlib import Path


TOOL_DIR = Path(__file__).with_name("tr-morph")

def morph_base(in_text, generate=False):
    """ Analyze the text using modified Kemal Oflazer's FST"""
    scr_path = "./%s/lm_tfeatures.scr" % ("synth" if generate else "anlyz")
    args = f"./lookup -f {scr_path}".split()
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

def morphological_generator(text):
    ret = morph_base(text, generate=True).split('\n')
    results = []
    intermediate = []
    for line in ret[:-1]:
        if not line:
            results.append(intermediate)
            intermediate = []
            continue
        res = line.split("\t")
        if len(res) == 3:
            _, _, gen_word = res
        else:
            _, gen_word = res
        if gen_word != "*UNKNOWN*":
            intermediate.append(gen_word)
    return results



