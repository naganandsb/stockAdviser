# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 12:08:01 2024

@author: Dell
"""

import matplotlib.pyplot as mp
import numpy as np
import pandas as pd
import specialops as so

def AutomobileSector(data,**kw):
    fig, axes = mp.subplots(nrows=4, ncols=1)
    fig.suptitle(data.get("company_url"))
    axes[0].plot(so.convertToFloat(data, "shareholding_Promoters", "%"),label = "shareholding_Promoters")
    axes[1].plot(so.convertToInt(data, "profit-loss_Sales", ","),label = "profit-loss_Sales")
    axes[2].plot(so.convertToInt(data, "quarters_Sales", ","),label = "quarters_Sales")
    axes[3].plot(so.convertToInt(data, "quarters_Net Profit", ","),label = "quarters_Net Profit") 
    mp.show()