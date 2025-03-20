    
class Catalog:
    """
    Le composant Catalog contient :
        - l'état du Système
        - Les données statistiques (selectivité et nombre de tuples)
        - Des méthodes pour mettre à jour ses informations

    """
    def __init__(self, dbs, wrps, hist_annee, hist_dept, hist_region, api_1_hist_annee, api_1_hist_dept, api_1_hist_region):
        self.databases = dbs
        self.wrappers = wrps
        self.catalog = {
                        "MEDIATOR" : {"JOIN" : 0.01}, 
                        "WRAPPER" : 0.05, 
                        "LOCALDBS" : { 
                                        "DB1" : {"TOTAL_TUPLES" : 38035, "ANNEE" : api_1_hist_annee, "DEPT" : api_1_hist_dept, "REGION" : api_1_hist_region},
                                        "DB2" : {"TOTAL_TUPLES" : 15026, "ANNEE" : hist_annee, "DEPT" : hist_dept, "REGION" : hist_region}}
                        }#Ce dictionnaire représente les histogrammes pour chaque base de données, il devrait être passé entre parenthèses
        self.parameters = {
                            "DB1" : {1 : [0.5782, 0, 0.0001807], 2 : [0.6077, 0, 0.0000751 ], 3 : [0.4740 , 0, 0.0011766]},
                            "DB2" : {1 : [0.3535, 0, 0.0028585], 2 : [0.5630, 0, 0.0034527], 3 : [2.3042 , 0, 0.0046127]}

                        }
    
    def compute_columns(self) :
        columns = set()

        for db in self.databases :
            for name in db.columns :
                columns.add(name)
        
        return list(columns)

    
    def get_catalog(self):
        return self.catalog
    
    def get_databases(self):
        return self.databases
    
    def get_wrappers(self):
        return self.wrappers


if __name__ == "__main__" :
    print("test catalog :")