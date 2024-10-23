import datetime as dt 
import requests as rq
import json
import pandas as pd 
import time
import numpy as np
import psutil
import os
import csv
import re 
from sqlite3 import connect


from server.adapters import EnergyAdapter1,EnergyAdapter2,PopulationAdapter,LogementAdapter


# Mediator

class InformationMediator:
    def __init__(self):
        self.energy_adapter1 =  EnergyAdapter1()
        self.energy_adapter2 =  EnergyAdapter2()
        self.population_adapter = PopulationAdapter()
        self.Logement_adapter = LogementAdapter()
    
    def get_API1_data(self):
        return pd.DataFrame(self.energy_adapter1.get_energy_production())    
    def get_API2_data(self):
        return pd.DataFrame(self.energy_adapter2.get_energy_production())        
    def get_API3_data(self):
        return pd.DataFrame(self.population_adapter.get_population())
    def get_API4_data(self):
        return pd.DataFrame(self.Logement_adapter.API_Logement_sociaux_bailleurs())
    
    def restriction(self, Query, dfs):
        start, end = "WHERE", ""
        conds = Query[Query.find(start) + len(start):Query.rfind(end)].strip().split(' and ')
        pattern = r'[<>=!]=?'
        matches = [re.findall(pattern, cond)[0] for cond in conds]
        
        conds_by_df = [[] for _ in dfs]
        df_cols = [df.columns for df in dfs]

        for cond in conds:
            col_name = cond.split(f'{re.findall(pattern, cond)[0]}')[0].strip()
            for idx, cols in enumerate(df_cols):
                if col_name in cols:
                    conds_by_df[idx].append(cond)

        conds_by_df_str = [' and '.join(conds) for conds in conds_by_df]

        queries = [
            f""" SELECT * FROM df{i+1} WHERE {conds_by_df_str[i]} """
            if len(conds_by_df_str[i]) > 0 else None
            for i in range(len(dfs))
        ]

        conn = connect(':memory:')

        for i, df in enumerate(dfs):
            if queries[i]:
                df.to_sql(f'df{i+1}', conn)
                dfs[i] = pd.read_sql(queries[i], conn)

        """ for i, df in enumerate(dfs): affichage
            if len(conds_by_df_str[i]) > 0:
                print(f"\n Shape après la sélection pour API_{i+1}")
                print(f"{df.shape} = 𝜎_{conds_by_df_str[i]}_(API_{i+1})") """

        return dfs
    
    
    def projection(self, list_apis, query):
        start, end = 'SELECT', 'FROM'
        cols_in_query = query[query.find(start)+len(start):query.rfind(end)].strip().split(', ')
    
        result_apis = [[] for _ in list_apis]
        
        for word in cols_in_query:
            for i, api_list in enumerate(list_apis):
                if word in api_list:
                    result_apis[i].append(word)
        
        return result_apis
    
    def jointure(self, dfs, list_apis):
        
        dfs_to_join = [df for df, api in zip(dfs, list_apis) if len(api) > 1]
        api_indices = [i+1 for i, api in enumerate(list_apis) if len(api) > 1]

        df_final = dfs_to_join[0]
        for df_to_join in dfs_to_join[1:]:
            df_final = pd.merge(df_final, df_to_join, on='region')

        
        if len(dfs_to_join) > 1:
            apis_involved = " ⋈ ".join([f"API_{i}" for i in api_indices])
            print(f"\n {df_final.shape} = ({apis_involved})")
        else:
            print(f"\n {df_final.shape} = (API_{api_indices[0]})")

        return df_final  
    
    
    
    def data(self, Query):
        print('\n ---------------- Initial shapes start ----------------')
        
        informationMediator = InformationMediator()
        dfs = [informationMediator.get_API1_data(),  
            informationMediator.get_API2_data(),  
            informationMediator.get_API3_data(),
            informationMediator.get_API4_data()]

        for i, df in enumerate(dfs):
            print(f" API_{i+1} : {df.shape}")
        print('\n ---------------- Initial shapes end ----------------')

        # La sélection (σ) 
        print('\n ---------------- 𝜎 start  ----------------')
        if 'WHERE' in Query:
            print("\n Sélection d'abord par conditions")
            dfs = self.restriction(Query, *dfs)  # Utilisation de la version généralisée de restriction
        else:
            print("\n Pas de conditions sur les APIs")
        print('\n ---------------- 𝜎 end ----------------')

        # La projection (Π)
        print('\n ---------------- Π start ----------------')
        list_apis = [df.columns for df in dfs]
        

        projected_apis = self.projection(list_apis, Query)
        
        for i in range(len(dfs)):
            dfs[i] = dfs[i][projected_apis[i]]
        
        print('\n Shapes après projection:')
        for i, df in enumerate(dfs):
            if len(projected_apis[i]) > 1:
                print(f"\n {df.shape} = Π_{projected_apis[i]}_(API_{i+1})")
        print('\n ---------------- Π end ----------------')

        # La jointure (⋈)
        print('\n ---------------- ⋈ start  ----------------')
        
        df_final = self.jointure(dfs, projected_apis)
        
        print('\n ---------------- ⋈ end ----------------')
        
        return df_final