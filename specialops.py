# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 12:25:39 2024

@author: Dell
"""

import numpy as np
import pandas as pd

def convertToFloat(data,field,spacial_chars):
    converted_list =[float(x.replace(spacial_chars,"")) for x in data.get(field)]
    return converted_list
def convertToInt(data,field,spacial_chars):
    converted_list =[int(x.replace(spacial_chars,"")) for x in data.get(field)]
    return converted_list
def converToSuitable(data):
    rm_special_list = [x.translate(str.maketrans("","",",%")) for x in data]
    float_or_int = [(x.find(".") != -1) for x in rm_special_list ]
    if(any(float_or_int)):
        try:
            return([float(x) for x in rm_special_list])
        except Exception as e:
            print(e)
            return rm_special_list
    else:
        try:
            return([int(x) for x in rm_special_list])
        except Exception as e:
            print(e)
            return rm_special_list
            