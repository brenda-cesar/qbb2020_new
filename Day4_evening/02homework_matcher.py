#!/usr/bin/env python3

import sys

import os.path 
from os import path
import gc 

def FASTAReader(_filePath: str, _kMerslength: int):  
    _resultDictionarylist = [] 
    _sequence = []
    _sequences = []
    _line = None 
    if not path.exists(_filePath):  
        print('file does not exists : {0}'.format(_filePath)) 
    else:
        _fastaFile = open(_filePath, 'r') 
        _line = _fastaFile.readline() 
        assert _line.startswith('>'),'Not a fasta file' 
        _seq_id = _line[1:].strip('\n\r') 
        _line = _fastaFile.readline() 
        while _line: 
            if _line.startswith('>'):
                _sequences.append((_seq_id,''.join(_sequence))) 
                _seq_id = _line[1:].rstrip('\n\r')
                _sequence = []
            else:
                _sequence.append(_line.strip()) 
            _line = _fastaFile.readline() 
        _sequences.append((_seq_id,''.join(_sequence))) 
        _seq_id = _line[1:].rstrip('\n\r') 
        for _SequenceId, _currentSequence in _sequences: 
            for _index in range(0, len(_currentSequence) - _kMerslength + 1):
                _kmerLower = _currentSequence[_index:(_index+_kMerslength)].strip().lower()
                _kmerUpper = _currentSequence[_index:(_index+_kMerslength)].strip().upper()
                _kmerItem = {   'SequenceId' : _SequenceId.strip(),'LowerKeyValue' : _kmerLower,'UpperValue': _kmerUpper,'IndexPosition': _index     }
                _resultDictionarylist.append(_kmerItem) 
    _sequence = None
    _sequences = None
    _line = None
    gc.collect() 
    return _resultDictionarylist 

import pandas as _pandas
import numpy as _numpy

def RunKmerMatcher(_targetFastaFilePath: str, _queryFastaFilePath: str, _kMerslength: int): 

    _targetDictionaryList = FASTAReader(_targetFastaFilePath, _kMerslength) 
    _queryDictionaryList = FASTAReader(_queryFastaFilePath, _kMerslength) 

    _targetDF = _pandas.DataFrame(_targetDictionaryList) 
    _queryDF = _pandas.DataFrame(_queryDictionaryList) 

    _targetDF.rename(columns={  'SequenceId': 'Target_SequenceId', 
                                'UpperValue': 'Target_UpperValue',\
                                'IndexPosition': 'Target_IndexPosition'}, inplace=True)
    _queryDF.rename(columns={   'SequenceId': 'Query_SequenceId',\
                                'UpperValue': 'Query_UpperValue',\
                                'IndexPosition': 'Query_IndexPosition'}, inplace=True)

    _targetDF.set_index('LowerKeyValue') 
    _queryDF.set_index('LowerKeyValue') 

    _kmerMatchesDataFrame = _pandas.merge(  _queryDF,_targetDF,how='inner',left_on=['LowerKeyValue'],right_on=['LowerKeyValue']).reset_index() 
    _targetDictionaryList = None 
    _queryDictionaryList = None
    _targetDF = None
    _queryDF = None
    gc.collect()

    _columnsNamesSingleLine = ''
    for _index, _row in _kmerMatchesDataFrame.iterrows(): 
        print('{0}\t{1}\t{2}'.format(_row['Target_SequenceId'],_row['Target_UpperValue'],_row['Target_IndexPosition']))


    return _kmerMatchesDataFrame

def main(_arg):
    if len(_arg) != 3:
        print('Invalid number of input arguments')
    else:
        RunKmerMatcher(_arg[0], _arg[1], int(_arg[2]))
if __name__ == "__main__":
    main(sys.argv[1:])