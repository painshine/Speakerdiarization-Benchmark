# Speaker Diarization Benchmark

> a toolkit for evaluation and detial analysis of speaker diarization algorithm

Contains Dataset: Aishell-4, VoxConverse, ICSI, AMI

## Installation

```bash
$ pip3 install simpleder
$ pip install textgrid
```

## Demo based on jupyter notebook

A simple demo [Demo.ipynb] is available to help you get started quickly. 

## Example

### Quatitative research
```bash
$ python cal_DER.py --dataset='aishell-4' --result_path='./test/aishell-4/' --MODE='EVAL' --details_analysis=TRUE
```

### Qualitative research
The plot tookit is integrated for qualitative research.
```bash
$ python cal_DER.py --WAV='./examples/S_R004S02C01.wav' --RES='./examples/S_R004S02C01.json' --SAVE_PATH='./examples/examples.png'
```

The output files for Quatitative research are '[dataset]_evalutaion.txt' and '[dataset]_detail.json'.

The output files for Qualitative research is './examples/examples.png'.

## Reference.
1.https://github.com/cvqluu/simple_diarizer
2.https://github.com/pyannote/pyannote-audio
