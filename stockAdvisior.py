# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:44:52 2024

@author: Dell
"""

import datacollector as dc
import analyzer 

an = analyzer.Analyzer()
companies_data = dc.getCompaniesData("/company/TATAMOTORS/consolidated/",fresh=False)
an.analyse(companies_data)
