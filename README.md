# Speaker Diarization Benchmark

> a toolkit for evaluation and detial analysis of speaker diarization algorithm

Contains Dataset: Aishell-4, VoxConverse, ICSI, AMI


## Installation

```bash
$ pip3 install simpleder
$ pip install pyannote.metrics
$ pip install pyannote.core
$ conda install -c roebel pysndfile
$ pip install librosa
```


## Example

### Quatitative research
```bash
$ python cal_DER.py --dataset='aishell-4' --result_path='./test/aishell-4/' --MODE='EVAL' --details_analysis=TRUE
```

### Qualitative research
The plot tookit is integrated for qualitative research.
```bash
$ python res_PLOT.py --WAV='./examples/WAV_FILE.wav' --RES='./examples/RES_FILE.json' --SAVE_PATH='./examples/examples.png'
```
![image](https://github.com/painshine/speaker_diarization_benchmark/blob/main/examples/examples.png)

### Save results

1.The output files for Quatitative research are '[dataset]_evalutaion.txt' and '[dataset]_detail.json'.

2.The output files for Qualitative research is './examples/examples.png'.


## Demo based on jupyter notebook

A simple demo [Demo.ipynb] is available to help you get started quickly. 


## Reference.
1.https://github.com/cvqluu/simple_diarizer

2.https://github.com/pyannote/pyannote-audio
