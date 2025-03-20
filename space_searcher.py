import _more as more
import networkx as nx
import re


class SpaceSearcher:
    
    """
    Le space searcher est programmé pour suivre 3 scénarios car le développer demanderait
    beaucoup de temps et le sujet se concentre surtout sur le modèle de coût.
    Ces trois scénarios sont les trois méthodes plan_i implémentées ci-dessous.
    """

    def __init__(self, catalog):
        self.catalog = catalog
        


    def plan1(self, databases, commande, attributs_commande, op_cls, val_cls, attributs_cls, classe):


        assert isinstance(databases, list), "databases doit être une liste"
        assert all(isinstance(db, more.Database) for db in databases), "Tous les éléments de databases doivent être de type more.Database"
        #assert isinstance(attributs_select, list), "attributs_select doit être une liste"
        #assert all(isinstance(attr, str) for attr in attributs_select), "Tous les éléments de attributs_select doivent être des chaînes de caractères"
        #assert isinstance(attributs_where, list), "attributs_where doit être une liste"
        #assert all(isinstance(attr, str) for attr in attributs_where), "Tous les éléments de attributs_where doivent être des chaînes de caractères"
        
        """
        Retourne un plan sous la forme d'un graphe NetworkX dont toutes
        les restrictions (attributs_where) d'une requête se font sur les
        bases de données locales. Si les attributs de la projection (attributs_select)
        sont répartis sur plusieurs bases de données locales, le join qui permet d'obtenir
        la relation globale se fait au niveau du médiateur.

        -------------------------------
        Inputs

        - databases : liste de databases de type more.Database()
        - attributs_select : liste d'attributs de type string
        - attributs_where : liste d'attributs de type string

        -------------------------------
        Output

        - Un graphe Networkx contenant les différentes opérations de la requête
        """ 
        tree = nx.DiGraph()
        tree.graph['class'] = classe
        noeud_join = more.Node(niv="MEDIATOR", is_glb_join = True, attr_cls_global_join = "ANNEE")
        tree.add_node(noeud_join, data=noeud_join)
        #Base de données locales
        for db in databases :
            #if bool(set(db.columns) & set(attributs_select)) :
            noeud = more.Node(niv="LOCALDBS", db=db.name, cmd=commande, attr_cmd=attributs_commande, 
                              is_whr= True, attr_cls_where = attributs_cls, op_cls_where = op_cls, val_cls_where=val_cls)
            tree.add_node(noeud, data=noeud)
            tree.add_edges_from([(noeud_join, noeud)])
        return tree

    def plan2(self, wrappers, commande, attributs_commande, op_cls, val_cls, attributs_cls, classe):
        tree = nx.DiGraph()
        tree.graph['class'] = classe
        noeud_join = more.Node(niv="MEDIATOR", is_glb_join = True, attr_cls_global_join = "ANNEE")
        tree.add_node(noeud_join, data=noeud_join)
        #Adaptateurs
        for wr in wrappers : 
            noeud = more.Node(niv="WRAPPER", wrps=wr.name, cmd=commande, attr_cmd=attributs_commande, 
                              is_whr= True, attr_cls_where = attributs_cls, op_cls_where = op_cls, val_cls_where=val_cls)
            tree.add_node(noeud, data=noeud)
            tree.add_edges_from([(noeud_join, noeud)])
            
        return tree
    

    def plan3(self, commande, attributs_commande, op_cls, val_cls, attributs_cls, classe):
        tree = nx.DiGraph()
        tree.graph['class'] = classe
        noeud_join = more.Node(niv="MEDIATOR", is_glb_join = True, attr_cls_global_join = "ANNEE")
        tree.add_node(noeud_join, data=noeud_join)
        #Adaptateurs
        
        noeud = more.Node(niv="WRAPPER", wrps="WRP1", cmd=commande, attr_cmd=attributs_commande, 
                            is_whr= True, attr_cls_where = attributs_cls, op_cls_where = op_cls, val_cls_where=val_cls)
        tree.add_node(noeud, data=noeud)
        tree.add_edges_from([(noeud_join, noeud)])
        
        
        noeud = more.Node(niv="LOCALDBS", db="DB2", cmd=commande, attr_cmd=attributs_commande, 
                              is_whr= True, attr_cls_where = attributs_cls, op_cls_where = op_cls, val_cls_where=val_cls)
        tree.add_node(noeud, data=noeud)
        tree.add_edges_from([(noeud_join, noeud)])

        return tree
    

    
    def search_space_computation_select(self, query):

        #Détecter les bases de données locales qui contiennent les attributs de la requêtes
        attributs = query.get_attributs_commandes()
        query_databases = []
        databases = self.catalog.get_databases()
        wrappers = self.catalog.get_wrappers()
        classe = query.get_class()

        for attribut in attributs :
            for db in databases :
                if db.is_in_database(attribut):
                    query_databases.append(db)
        
        # Expression régulière pour capturer l'attribut et la valeur
        match = re.search(r"WHERE\s+(\w+)\s*=\s*'([^']*)'", query.get_condition())
        if match:
            attributs_cls = match.group(1)
            val_cls = match.group(2)
        op_cls = '='
        commande =  query.get_commande()
        attributs_commande = query.get_attributs_commandes()

        tree1 = self.plan1(databases, commande, attributs_commande, op_cls, val_cls, [attributs_cls], classe)

        tree2 = self.plan2(wrappers, commande, attributs_commande, op_cls, val_cls, [attributs_cls], classe)

        tree3 = self.plan3(commande, attributs_commande, op_cls, val_cls, [attributs_cls], classe)


        return [tree1, tree2, tree3]
   
        
if __name__ == "__main__" :
    print("test space searcher")



        