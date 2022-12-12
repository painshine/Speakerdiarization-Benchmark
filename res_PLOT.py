"""Qualitative research for benchmark.

Authors
 * Runqing Zhang 2022

Example
 * python cal_DER.py --WAV='./examples/S_R004S02C01.wav' --RES='./examples/S_R004S02C01.json' --SAVE_PATH='./examples/examples.png'
 
Note
 * RES Format:
 * [{'start': 8.43,
 * 'end': 10.12,
 * 'label': 1,
 * 'start_sample': 134880,
 * 'end_sample': 161920}]

Attention
 * If the format of your results is not same as ours,
 * you can add the format conversion function in utils.py
 * A example [convert_ss] is shown in utils.py
 * The details for stadard format are shown in utils.py 

 * For the detail analysis, the save file is 'output_log.json'

"""

#include
import json
import argparse
import functools
import utils
import soundfile as sf
import matplotlib.pyplot as plt
from plottookits import combined_waveplot

#Input parameters
parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(utils.add_arguments, argparser=parser)
add_arg('WAV',       str,  './examples/S_R004S02C01.wav',      "WAV file path")
add_arg('RES',       str,  './examples/S_R004S02C01.json',     "Results path")
add_arg('SAVE_PATH', str,  './examples/examples.png',          "Save path")
args = parser.parse_args()

if __name__ == "__main__":
    #Setting Save Path
    save_path = args.SAVE_PATH
    
    #Example:
    #wav file:     ./examlpes/S_R004S02C01.wav
    #result file:  ./examples/S_R004S02C01.json
    WAV_FILE = args.WAV
    RES_FILE = args.RES
    
    #Load Result
    with open(RES_FILE, 'r', encoding = 'utf8') as fp:   #读取第j段的局部说话人日志
        diar = json.load(fp)
        
    #Read WAV FILE
    signal, fs = sf.read(WAV_FILE)
    combined_waveplot(signal, fs, diar)
    plt.savefig(save_path, bbox_inches='tight')
    #plt.show()
