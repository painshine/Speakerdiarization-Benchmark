"""Convert the prediction results into a standard format for evaluation.

Authors
 * Runqing Zhang 2022

Example
 * stadard groundtruth:
 *
 * reference = Annotation()
 * reference[Segment(0, 10)] = 'A'
 * reference[Segment(30, 40)] = 'C'
 * reference[Segment(8, 20)] = 'B'
 * reference[Segment(24, 27)] = 'A'
 
 * The stadard format of a result item is same as the stadard groundtruth.

"""
import distutils.util
from pyannote.core import Annotation, Segment

#Aishell-4 groundtruth
def convert_aishell4(all_the_text):
    reference = Annotation()
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        if _tem != '':
            _cont = _tem.split(' ')
            _spk_id = _cont[2]
            _start = round(float(_cont[3]) * 16000)
            _end = round(float(_cont[4]) * 16000)
            
            reference[Segment(_start, _end)] = _spk_id
    return reference

#VoxConverse groundtruth
def convert_vox(all_the_text):
    reference = Annotation()
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        if _tem != '':
            _cont = _tem.split(' ')
            _spk_id = _cont[-3]
            _start = round(float(_cont[3]) * 16000)
            _end = round((float(_cont[3]) + float(_cont[4])) * 16000)
            
            reference[Segment(_start, _end)] = _spk_id
    return reference

#ICSI groundtruth
def convert_icsi(all_the_text):
    reference = Annotation()
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        _head = _tem.split(' StartTime=')[0]
        if ('Segment' in _head) and ('CloseMic' not in _tem) and ('Channel' not in _tem):
            #print(_tem)
            _cont1 = _tem.split('StartTime="')[-1]
            _start = _cont1.split('" EndTime=')[0]
            #print(_start)
            _cont2 = _tem.split('EndTime="')[-1]
            _end = _cont2.split('" Participant=')[0]
            #print(_end)
            _cont3 = _tem.split('Participant="')[-1]
            _spk_id = _cont3.split('">')[0]
            #print(_start, _end, _spk_id)

            _start = round(float(_start) * 16000)
            _end = round(float(_end) * 16000)
            
            reference[Segment(_start, _end)] = _spk_id
    return reference

#AMI groundtruth
def convert_ami(all_the_text):
    reference = Annotation()
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        if (_tem != '') and ('channel' not in _tem):
            _start = _tem.split(',')[0]
            _end = _tem.split(',')[1]
            _spk_id = _tem.split(',')[2]
            
            _start = round(float(_start) * 16000)
            _end = round(float(_end) * 16000)
            
            reference[Segment(_start, _end)] = _spk_id
    return reference

#Record Speaker id
def countspk_aishell4(all_the_text):
    _tem_list = all_the_text.split('\n')
    spk_list = []
    for _tem in _tem_list:
        if _tem != '':
            _cont = _tem.split(' ')
            _spk_id = _cont[2]
            if _spk_id not in spk_list:
                spk_list.append(_spk_id)
    return spk_list

def countspk_vox(all_the_text):
    _tem_list = all_the_text.split('\n')
    spk_list = []
    for _tem in _tem_list:
        if _tem != '':
            _cont = _tem.split(' ')
            _spk_id = _cont[-3]
            if _spk_id not in spk_list:
                spk_list.append(_spk_id)
    return spk_list

def countspk_icsi(all_the_text):
    _tem_list = all_the_text.split('\n')
    spk_list = []
    for _tem in _tem_list:
        _head = _tem.split(' StartTime=')[0]
        if ('Segment' in _head) and ('CloseMic' not in _tem) and ('Channel' not in _tem):
            _cont3 = _tem.split('Participant="')[-1]
            _spk_id = _cont3.split('">')[0]
            if _spk_id not in spk_list:
                spk_list.append(_spk_id)
    return spk_list

def countspk_ami(all_the_text):
    _tem_list = all_the_text.split('\n')
    spk_list = []
    for _tem in _tem_list:
        if (_tem != '') and ('channel' not in _tem):
            _spk_id = _tem.split(',')[2]
            if _spk_id not in spk_list:
                spk_list.append(_spk_id)
    return spk_list

#Self Search Result:
def convert_ss(json):
    hypothesis = Annotation()
    diar = json
    for _diar in diar:
        #_data = (str(_diar['label']), _diar['start'], _diar['end'])
        hypothesis[Segment(_diar['start_sample'], _diar['end_sample'])] = str(_diar['label'])
    return hypothesis

##other functions

#add arguments
def add_arguments(argname, type, default, help, argparser, **kwargs):
    type = distutils.util.strtobool if type == bool else type
    argparser.add_argument("--" + argname,
                           default=default,
                           type=type,
                           help=help + ' 默认: %(default)s.',
                           **kwargs)
    
#Aishell-4 diar
def diar_aishell4(all_the_text):
    diar = []
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        diar_tem = {}
        if _tem != '':
            _cont = _tem.split(' ')
            _spk_id = _cont[2]
            _start = round(float(_cont[3]) * 16000)
            _end = round(float(_cont[4]) * 16000)
            
            diar_tem['label'] = _spk_id
            diar_tem['start'] = float(_cont[3])
            diar_tem['end'] = float(_cont[4])
            diar.append(diar_tem)
    return diar

#VoxConverse diar
def diar_vox(all_the_text):
    diar = []
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        diar_tem = {}
        if _tem != '':
            _cont = _tem.split(' ')
            _spk_id = _cont[-3]
            _start = round(float(_cont[3]) * 16000)
            _end = round((float(_cont[3]) + float(_cont[4])) * 16000)
            
            diar_tem['label'] = _spk_id
            diar_tem['start'] = float(_cont[3])
            diar_tem['end'] = float(_cont[4]) + float(_cont[3])
            diar.append(diar_tem)
    return diar

#ICSI diar
def diar_icsi(all_the_text):
    diar = []
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        diar_tem = {}
        _head = _tem.split(' StartTime=')[0]
        if ('Segment' in _head) and ('CloseMic' not in _tem) and ('Channel' not in _tem):
            _cont1 = _tem.split('StartTime="')[-1]
            _start = _cont1.split('" EndTime=')[0]
            
            _cont2 = _tem.split('EndTime="')[-1]
            _end = _cont2.split('" Participant=')[0]
            
            _cont3 = _tem.split('Participant="')[-1]
            _spk_id = _cont3.split('">')[0]

            _start = round(float(_start) * 16000)
            _end = round(float(_end) * 16000)
            
            diar_tem['label'] = _spk_id
            diar_tem['start'] = float(_cont1.split('" EndTime=')[0])
            diar_tem['end'] = float(_cont2.split('" Participant=')[0])
            diar.append(diar_tem)
    return diar

#AMI diar
def diar_ami(all_the_text):
    diar = []
    _tem_list = all_the_text.split('\n')
    for _tem in _tem_list:
        diar_tem = {}
        if (_tem != '') and ('channel' not in _tem):
            diar_tem['label'] = _tem.split(',')[2]
            diar_tem['start'] = float(_tem.split(',')[0])
            diar_tem['end'] = float(_tem.split(',')[1])
            
            diar.append(diar_tem)
    return diar

#calculate overlap time
def overlap_rate(diar):
    overlap_time = 0
    total_time = 0
    for _index, _diari in enumerate(diar):       
        rest_diar = diar[_index+1:]
        
        time_dura = _diari['end'] - _diari['start']
        total_time = total_time + time_dura
        
        for _diarj in rest_diar:
            _starti = _diari['start']
            _endi = _diari['end']
            
            _startj = _diarj['start']
            _endj = _diarj['end']
            
            if (_startj < _starti < _endj) and (_endi > _endj):
                _opt = _endj - _starti
            elif (_startj < _endi < _endj) and (_starti < _startj):
                _opt = _endi - _startj
            elif (_starti > _startj) and (_endi < _endj):
                _opt = _endi - _starti
            else:
                _opt = 0
            overlap_time = overlap_time + _opt
    if (total_time - overlap_time) == 0:
        over_rate = 0
    else:
        over_rate = overlap_time / (total_time - overlap_time)
    over_rate = round(over_rate * 100, 2)
    return over_rate
            
            
        