"""
Fonctions utiles et structures de données nécessaires
"""

class Node:

    niveaux = ["MEDIATOR","WRAPPER" ,"LOCALDBS"]
    commandes = ["SELECT", "INSERT", "UPDATE", "DELETE"]

    def __init__(self, niv, wrps = None, db = None, cmd=None, attr_cmd=None,
                 is_whr=False, attr_cls_where=None,  op_cls_where=None,  val_cls_where=None,
                 is_inner_jnt=False, op_cls_global_join=None, attr_cls_global_join=None,
                 is_glb_join = False, op_cls_inner_join=None, attr_cls_inner_join=None
                 ):
        
        #assert niv in Node.niveaux, "Niveau noeud ne correspond pas"
        #assert not is_whr or attr_cls_where, "Si is_whr est vrai, alors attr_cls_where doit être vrai"
        #assert cmd in Node.commandes, "Commande noeud ne correspond pas"
        #assert attr_cmd, attr_cls in attributs
        #assert (bool(jnt) != bool(aggr)) or (not jnt and not aggr)
        
        #Niveau du système
        self.niveau = niv
        self.wrappers = wrps
        self.database = db
        
        #Commande (SELECT, INSERT, UPDATE, DELETE)
        self.commande = cmd
        self.attribut_commande = attr_cmd #peut être une liste
        
        #Types de clause 
        self.is_where = is_whr
        self.is_inner_jointure = is_inner_jnt
        self.is_global_join = is_glb_join

        #self.is_having = is_hvg
        #self.is_groupby = is_grpby
        #self.is_orderby = is_ordby (ces clauses seront à déclarer ultérieurement)

        self.operator_clause_where = op_cls_where
        self.attributs_clause_where = attr_cls_where
        self.valeur_clause_where = val_cls_where

        self.operator_global_join = op_cls_global_join
        self.attributs_global_join = attr_cls_global_join

        self.operator_inner_join = op_cls_inner_join
        self.attributs_inner_join = attr_cls_inner_join

        #Cout
        self.cout = None
    
    def __str__(self):
        """Affiche uniquement les attributs non vides."""
        attributes = {k: v for k, v in vars(self).items() if v is not None}
        return "\n".join(f"{k}: {v}" for k, v in attributes.items())


class Query():

    def __init__(self, cmd , attr_cmd, tbls, classe, cond = None):
        self.commande =  cmd
        self.attributs_commandes = attr_cmd #Pour un select : * ou liste attributs, pour un Update table, pour un Insert table etc..
        self.condition = cond
        self.tables = tbls
        self.classe = classe

    #Getters
           
    def get_commande(self):
        return self.commande
    
    def get_attributs_commandes(self):
        return self.attributs_commandes
    
    def get_condition(self):
        return self.condition
    
    def get_tables(self):
        return self.tables
    
    def get_class(self):
        return self.classe
    
    #Methods

    def is_condition(self):
        return False if self.condition is None else True

class Wrapper():
    
    def __init__(self, name, columns) :
        self.name = name
        self.columns = columns

class Table():

    def __init__(self, name, columns) :
        self.name = name
        self.columns = columns

class Database():

    def __init__(self, name, columns, url) :
        self.name = name
        self.columns = columns
        self.url = url

    def is_in_database(self, attribut) :
        return attribut in self.columns


if __name__ == "__main__" :
    print("Test _more")

