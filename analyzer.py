# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 09:23:56 2024

@author: Dell
"""

import automobile
import pandas as pd

class Analyzer:
    def analyse(self,datacollection,**kw):
        companies_df = pd.DataFrame(datacollection)
        print(companies_df["quarters_Sales"].describe())
        
        # for d in datacollection:
        #     sector = d.get("Sector")
        #     match sector:
        #         case "Automobile":
        #               automobile.AutomobileSector(d,**kw)
        #         case _:
        #             print("Normal")
                
        
            
        