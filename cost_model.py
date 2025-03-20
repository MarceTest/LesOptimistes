import networkx as nx


class CostModel:
    
    """
    Prend un plan d'exécution et calcul son coût.
    Pour le moment, et pour simplifier le code, on va juste renvoyer un cout global.

    """
    def __init__(self, catalog):
        self.catalog = catalog

    def cost_mediator(self, node, catalog, classe) :
        if node.is_global_join :
            node.cout = catalog.catalog["MEDIATOR"]["JOIN"]
        else :
            print("Médiateur : rien pour l'instant")
        
        return node.cout

    def cost_wrapper(self, node, catalog, classe) :
        node.cout = catalog.catalog["WRAPPER"]

        return node.cout
        

    def cost_localdbs(self, node, catalog, classe):
        
        db = node.database
        
        val_clause = node.valeur_clause_where
        op_cls = node.operator_clause_where

        for elem in node.attributs_clause_where : #astuce pour récupérer la string du set, à enlever
            attr_clause = elem
        
        match op_cls :
            case "=":
                #pour l'instant on test avec op = "="
                local_total = catalog.catalog["LOCALDBS"][db][attr_clause][val_clause]["Nombre"]
                total = catalog.catalog["LOCALDBS"][db]["TOTAL_TUPLES"]
                selectivity = local_total / total
                cost_function = catalog.parameters[db][classe][0] + catalog.parameters[db][classe][1] * \
                                                                total + catalog.parameters[db][classe][2] * selectivity
                node.cout = cost_function
            case ">":
                pass
            case ">=":
                pass
            case "<":
                pass
            case "<=":
                pass

        return node.cout
    
    def global_cost(self, tree):
        total_cost = 0
        classe = tree.graph['class']

        for node in tree.nodes:  # Assure un parcours des dépendances
            if node.niveau == "MEDIATOR":
                node_cost = self.cost_mediator(node, self.catalog, classe)
            elif node.niveau == "WRAPPER":
                node_cost = self.cost_wrapper(node, self.catalog, classe)
            elif node.niveau == "LOCALDBS":
                node_cost = self.cost_localdbs(node, self.catalog, classe)
            else:
                node_cost = 0  # Par défaut, aucun coût

            total_cost += node_cost  # Ajouter au coût total

        return total_cost


