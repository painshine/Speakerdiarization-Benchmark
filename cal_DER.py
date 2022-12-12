"""Calculate DER for benchmark.

Authors
 * Runqing Zhang 2022

Example
 * python cal_DER.py --dataset='aishell-4' --result_path='./test/results/' --MODE='EVAL' --details_analysis=False
 
Note
 * Usually, MODE should be 'EVAL'
 * The default value of dataset is 'aishell-4'
 * The default result path is './test/results/'
 * This benchmark includes 4 datasets: Aishell-4, ICSI, AMI, VoxConvserse

Attention
 * If the format of your results is not same as ours,
 * you can add the format conversion function in utils.py
 * A example [convert_ss] is shown in utils.py
 * The details for stadard format are shown in utils.py 

 * For the detail analysis, the save file is 'output_log.json'

"""

import simpleder
import functools
import json
import os
import numpy as np
import argparse

import utils
from pyannote.metrics.diarization import DiarizationErrorRate, DiarizationPurity, DiarizationCoverage

#Input parameters
parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(utils.add_arguments, argparser=parser)
add_arg('dataset',           str,  'aishell-4',        "dataset for evaluation:aishell-4, voxconverse, ICSI, AMI")
add_arg('result_path',       str,  './test/results/',  "results path")
add_arg('MODE',              str,  'EVAL',             "MODE, EVAL or TEST")
add_arg('details_analysis',  bool,  False,             "True if you need detail analysis")
args = parser.parse_args()

if __name__ == "__main__":
    
    #Dataset name
    dataset = args.dataset
    #Prediction path
    result_path = args.result_path
    #Operating Mode
    _Mode = args.MODE # default: EVAL

    #Call format transformation function
    conv_res = utils.convert_ss
    
    #detail analysis
    if args.details_analysis:
        JSON_FILE = dataset + '_details.json'
        details = []
        
    #Choose dataset for evaluation: ['aishell-4', 'voxconvserse', 'ICSI']
    if dataset == 'aishell-4':
        conv_gt = utils.convert_aishell4
        gt_path = './datasets/aishell-4/'
    elif dataset == 'voxconverse':
        conv_gt = utils.convert_vox
        gt_path = './datasets/VoxConverse/'
    elif dataset == 'ICSI':
        conv_gt = utils.convert_icsi
        gt_path = './datasets/ICSI/'
    elif dataset == 'AMI':
        conv_gt = utils.convert_ami
        gt_path = './datasets/AMI/'
    else:
        raise ValueError('Cannot find Dataset!')

    #Check the results path
    if not os.path.exists(result_path):
        raise ValueError('Cannot find result path!')

    #Check the number of files
    result_list = os.listdir(result_path)
    gt_list = os.listdir(gt_path + 'gts/')
    if len(result_list) < len(gt_list):
        raise ValueError('Incomplete result files!')

    diarizationErrorRate = DiarizationErrorRate()
    purity = DiarizationPurity()
    coverage = DiarizationCoverage()

    #Evaluation
    DER_list = []
    Purity_list = []
    Coverage_list = []
    
    #output save file
    OUTPUT_FILE = dataset + '_evaluation.txt'
    f = open(OUTPUT_FILE,"a") 
    
    for _gt in gt_list:
        #Read gt file:
        
        #aishell-4
        if dataset == 'aishell-4':
            wav_name = _gt.split('.stm')[0]
            file_object = open(gt_path + 'gts/' + _gt)  
            gt_text = file_object.read()  
            file_object.close()
            
            gt = conv_gt(gt_text)
            
            #analysis overlap rate
            diar = utils.diar_aishell4(gt_text)
            overlap_rate = utils.overlap_rate(diar)
            
            #Count speaker id
            spk_list = utils.countspk_aishell4(gt_text)
            spk_num = len(spk_list)
        
        #VoxConverse
        elif dataset == 'voxconverse':
            wav_name = _gt.split('.rttm')[0]
            file_object = open(gt_path + 'gts/' + _gt)  
            gt_text = file_object.read()  
            file_object.close()
            
            gt = conv_gt(gt_text)
            
            #analysis overlap rate
            diar = utils.diar_vox(gt_text)
            overlap_rate = utils.overlap_rate(diar)
            
            #Count speaker id
            spk_list = utils.countspk_vox(gt_text)
            spk_num = len(spk_list)
            
        #ICSI
        elif dataset == 'ICSI':
            wav_name = _gt.split('.txt')[0]
            file_object = open(gt_path + 'gts/' + _gt)  
            gt_text = file_object.read()  
            file_object.close()
            
            gt = conv_gt(gt_text)
            
            #analysis overlap rate
            diar = utils.diar_icsi(gt_text)
            overlap_rate = utils.overlap_rate(diar)
            
            #Count speaker id
            spk_list = utils.countspk_icsi(gt_text)
            spk_num = len(spk_list)
            
        #AMI
        elif dataset == 'AMI':
            wav_name = _gt.split('.txt')[0]
            file_object = open(gt_path + 'gts/' + _gt)
            gt_text = file_object.read()
            file_object.close()
            
            gt = conv_gt(gt_text)
            
            #analysis overlap rate
            diar = utils.diar_ami(gt_text)
            overlap_rate = utils.overlap_rate(diar)
            
            #Count speaker id
            spk_list = utils.countspk_ami(gt_text)
            spk_num = len(spk_list)
            
        else:
            raise ValueError('Cannot find Dataset!')
        
        #TEST mode: for developers
        if _Mode == 'TEST':
            _type = '.stm'
            res_path = result_path + wav_name + _type

            #Check result file
            if not os.path.exists(res_path):
                raise ValueError('Cannot find ' + res_path)

            #Read result file
            file_object = open(res_path)  
            all_the_text = file_object.read()  
            file_object.close()

            #Convert Stadard result
            res = conv_gt(all_the_text)

        #EVAL mode: for experiments:
        elif _Mode == 'EVAL':
            _type = '.json'
            res_path = result_path + wav_name + _type

            #Check result file
            if not os.path.exists(res_path):
                raise ValueError('Cannot find result for ' + wav_name)

            #Read result file
            with open(res_path, 'r', encoding = 'utf8') as fp:   
                diar = json.load(fp)

            #Convert Stadard result
            res = conv_res(diar)

        else:
            raise ValueError('MODE ERROR! Only \'TEST\' or \'EVAL\' mode can be used!')

        #cal DER
        try:
            _DER = diarizationErrorRate(gt, res)
            _pur = purity(gt, res)
            _cov = coverage(gt, res)
            
            if overlap_rate == 0:
                _DER = 0
                _pur = 1
                _cov = 1
            
            if args.details_analysis:
                _detail = diarizationErrorRate(gt, res, detailed=True)
                _detail['wav'] = wav_name
        except:
            raise ValueError('DER calculate error for ' + wav_name + '!')
            
        #info for each wav
        _info = 'For ' + wav_name + '(' + str(spk_num) + ' Speakers, Overlap rate: ' + str(overlap_rate) + '%), DER is ' + str(_DER) + '.'
        print(_info)
        f.write(_info + '\n')
        
        #clear history
        res = []
        gt = []

        #collect
        DER_list.append(_DER)
        Purity_list.append(_pur)
        Coverage_list.append(_cov)
        
        #collect details
        if args.details_analysis:
            details.append(_detail)
            _detail = []

    #Calculate average DER, Clusters purity and coverage
    DER_list = np.array(DER_list)
    DER = np.sum(DER_list) / len(DER_list)
    
    Purity_list = np.array(Purity_list)
    Purity = np.sum(Purity_list) / len(Purity_list)
    
    Coverage_list = np.array(Coverage_list)
    Coverage = np.sum(Coverage_list) / len(Coverage_list)
    

    #print result info
    res_str1 = 'The average DER based on the Dataset ' + dataset + ' is ' + str(DER) + '.'
    res_str2 = 'The average Clusters purity based on the Dataset ' + dataset + ' is ' + str(Purity) + '.'
    res_str3 = 'The average Coverage based on the Dataset ' + dataset + ' is ' + str(Coverage) + '.'
    
    print(res_str1)
    print(res_str2)
    print(res_str3)
    f.write(res_str1 + '\n')
    f.write(res_str2 + '\n')
    f.write(res_str3 + '\n')
    
    f.close()
    
    #Save details
    if args.details_analysis:
        with open(JSON_FILE, "w") as f:
            f.write(json.dumps(details, ensure_ascii=False, indent=4, separators=(',', ':')))
