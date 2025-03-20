class Optimizer :
    """
    Rôle du composant Optimizer :
    - Parser une requête SQL
    - Créer un espace de recherche d'arbres algébriques
    - Récupérer les coûts de chaque opération
    - Choisir le meilleur plan
    """

    #--------INIT---------------
    
    def __init__(self, parser, space_searcher, cost_model):
        self.parser = parser
        self.space_searcher= space_searcher
        self.cost_model = cost_model
    
    #-------METHODS--------------
    
    def receive_query(self, query, classe):
        return self.parser.parse(query, classe) #de Type _more.Query()
    
    def compute_search_space(self, query):
        return self.space_searcher.search_space_computation_select(query)

    def display_cost_trees(self, search_space):
        cost_trees = []
        for tree in search_space :
            cost_trees.append(self.cost_model.global_cost(tree))

        return cost_trees


if __name__ == "__main__" :
    print("test optimizer :")
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    """def global_cost(self, arbre, catalog) :
        
        classe = self.which_class()
        
        cout_global =0
        for node in arbre.nodes() :
            match node.niveau :
                case "MEDIATOR" :
                    cout_global += self.cost_mediator(node, catalog, classe)
                case "WRAPPER" :
                    cout_global += self.cost_wrapper(node, catalog, classe)
                case "LOCALDBS" :
                    cout_global += self.cost_localdbs(node, catalog, classe)
       
        return cout_global"""    
    
    """
    db1 = more.Datatabase("DB1", ["REGION", "DEPT", "ANNEE", "REGION"], "www.db1.com")
    db2 = more.Datatabase("DB2", ["EPCI", "OP_GAZ", "ANNEE"], "www.db2.com")
    databases = [db1]
    wrp1 = more.Wrapper("wrp1", ["REGION", "ANNEE"])
    wrp2 = more.Wrapper("wrp2", ["EPCI", "ANNEE"])
    wrp3 = more.Wrapper("wrp3", ["DEPT", "ANNEE"])
    wrappers = [wrp1, wrp2, wrp3]
    dict_annee = {"2015": {'Nombre': 1255, 'Ratio': 0.08352189538133901}, "2016": {'Nombre': 1255, 'Ratio': 0.08352189538133901}, "2017": {'Nombre': 1255, 'Ratio': 0.08352189538133901}, "2022": {'Nombre': 1255, 'Ratio': 0.08352189538133901}, "2023": {'Nombre': 1255, 'Ratio': 0.08352189538133901}, "2020": {'Nombre': 1252, 'Ratio': 0.08332224144815653}, "2021": {'Nombre': 1252, 'Ratio': 0.08332224144815653}, "2013": {'Nombre': 1250, 'Ratio': 0.08318913882603488}, "2014": {'Nombre': 1250, 'Ratio': 0.08318913882603488}, "2012": {'Nombre': 1249, 'Ratio': 0.08312258751497405}, "2018": {'Nombre': 1249, 'Ratio': 0.08312258751497405}, "2019": {'Nombre': 1249, 'Ratio': 0.08312258751497405}}
    dict_dept = {'Aude': {'Nombre': 312, 'Ratio': 0.020764009050978305}, 'Bas-Rhin': {'Nombre': 276, 'Ratio': 0.0183681618527885}}
    dict_region = {'Auvergne-Rhône-Alpes': {'Nombre': 1955, 'Ratio': 0.13010781312391853}, 'Occitanie': {'Nombre': 1896, 'Ratio': 0.1261812857713297}, 'Nouvelle-Aquitaine': {'Nombre': 1818, 'Ratio': 0.12099028350858512}}
    
    requete2 = "SELECT REGION, EPCI WHERE ANNEE = '2020'"
    requete3 = "SELECT DEPT FROM Consommation WHERE ANNEE = '2020'"
    requetes = [requete1, requete2, requete3]

    trees = []
    decompte_requete = 0
    for requete in requetes :
        tree_1, tree_2 = optimizer1.parser(requete)
        #afficher les arbres
        # Dessiner le graphe
        # Générer les labels à partir des objets
        labels = {node: str(attr) for node, attr in nx.get_node_attributes(tree_1, "data").items()}
        # Dessiner le graphe
        pos = nx.spring_layout(tree_1)
        nx.draw(tree_1, pos, node_color='lightblue', node_size=3000)
        nx.draw_networkx_labels(tree_1, pos, labels, font_size=8, font_color="black")

        
        # Enregistrer l'image (format PNG)
        plt.savefig(f"avant{decompte_requete}", dpi=300)  # Enregistrement avec haute résolution
        plt.close()  # Fermer la figure après l'enregistrement

        labels = {node: str(attr) for node, attr in nx.get_node_attributes(tree_2, "data").items()}
        # Dessiner le graphe
        pos = nx.spring_layout(tree_2)
        nx.draw(tree_2, pos, node_color='lightblue', node_size=3000)
        nx.draw_networkx_labels(tree_2, pos, labels, font_size=8, font_color="black")
        # Enregistrer l'image (format PNG)
        plt.savefig(f"avant{decompte_requete}", dpi=300)  # Enregistrement avec haute résolution
        plt.close()  # Fermer la figure après l'enregistrement

        decompte_requete +=1

        trees.append((tree_1, tree_2))

    #cout
    for tree1, tree2 in trees :
        
        global_cost_tree_1 = optimizer1.global_cost(tree1, catalog)
        global_cost_tree_2 = optimizer1.global_cost(tree2, catalog)

        print(global_cost_tree_1)
        #afficher les arbres
        # Dessiner le graphe
        # Générer les labels à partir des objets
        labels = {node: str(attr) for node, attr in nx.get_node_attributes(tree1, "data").items()}
        # Dessiner le graphe
        pos = nx.spring_layout(tree1)
        nx.draw(tree1, pos, node_color='lightblue', node_size=3000)
        nx.draw_networkx_labels(tree1, pos, labels, font_size=8, font_color="black")
        # Enregistrer l'image (format PNG)
        plt.savefig(f"apres{decompte_requete}", dpi=300)  # Enregistrement avec haute résolution
        plt.close()  # Fermer la figure après l'enregistrement

        print(global_cost_tree_2)
        labels = {node: str(attr) for node, attr in nx.get_node_attributes(tree2, "data").items()}
        # Dessiner le graphe
        pos = nx.spring_layout(tree2)
        nx.draw(tree2, pos, node_color='lightblue', node_size=3000)
        nx.draw_networkx_labels(tree2, pos, labels, font_size=8, font_color="black")
        # Enregistrer l'image (format PNG)
        plt.savefig(f"apres{decompte_requete}", dpi=300)  # Enregistrement avec haute résolution
        plt.close()  # Fermer la figure après l'enregistrement

        decompte_requete +=1

        """
    



    
    



