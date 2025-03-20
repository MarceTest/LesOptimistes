#LIBRARIES
import argparse
import matplotlib.pyplot as plt
import json
import networkx as nx
import os

#MODULES
import cost_model
import _more as more
import catalog
import parser
import space_searcher
import optimizer

#---------------------------------------------MAIN------------------------------------------------------------

#--------------PARSER------------------
parser = parser.Parser()

#--------------CATALOG------------------

# Charger le fichier JSON
fichiers = ["hist_annee.json", "hist_dept.json", "hist_region.json", "api_1_hist_region.json", "api_1_hist_dept.json", "api_1_hist_annee.json"]
repo = "json_files/"
variables = {}

# Chargement des fichiers JSON et assignation aux variables
for fichier in fichiers:
    with open(repo+fichier, "r", encoding="utf-8") as f:
        var_name = fichier.replace(".json", "")  # Nom de la variable sans extension
        variables[var_name] = json.load(f)

# Assignation des variables en dehors du dictionnaire si nécessaire
hist_annee = variables["hist_annee"]
hist_dept = variables["hist_dept"]
hist_region = variables["hist_region"]
api_1_hist_annee = variables["api_1_hist_annee"]
api_1_hist_dept = variables["api_1_hist_dept"]
api_1_hist_region = variables["api_1_hist_region"]
db1 = more.Database('DB1', ['ANNEE', 'DEPT'], "www.db1.com")
db2 = more.Database('DB2', ['REGION'], "www.db2.com")
wrp1 = more.Wrapper('wrp1', ['ANNEE', 'DEPT'])
wrp2 = more.Wrapper('wrp2', ['REGION'])
databases = [db1, db2]
wrappers = [wrp1, wrp2]
catalog = catalog.Catalog(databases, wrappers, hist_annee, hist_dept, hist_region, api_1_hist_annee, api_1_hist_dept, api_1_hist_region)

#-------------SPACE_SEARCHER-------------
space_searcher = space_searcher.SpaceSearcher(catalog=catalog)

#-------------COST_MODEL-----------------
cost_model = cost_model.CostModel(catalog)

#------------OPTIMIZER-------------------
optimiseur = optimizer.Optimizer(parser, space_searcher, cost_model)

#-----------Récupérer la requête-----------------
arguments_parser = argparse.ArgumentParser(description="Exécute une requête avec sa classe")
arguments_parser.add_argument("query", type=str, help="The SQL query to execute.")
arguments_parser.add_argument("class_number", type=int, help="The class number for the query.")
args = arguments_parser.parse_args()

query = optimiseur.receive_query(args.query, args.class_number)

search_space = optimiseur.compute_search_space(query)

output_dir = "trees"

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i, tree in enumerate(search_space):
# Extract labels from node attributes
    labels = {node: str(attr) for node, attr in nx.get_node_attributes(tree, "data").items()}
    
    # Set a larger figure size to avoid cropping
    plt.figure(figsize=(10, 10))  # Adjust width and height as needed
    
    # Draw the graph
    pos = nx.spring_layout(tree)
    nx.draw(tree, pos, node_color='lightblue', node_size=5000)
    nx.draw_networkx_labels(tree, pos, labels, font_size=8, font_color="black")
    
    # Save the image (PNG format)
    plt.savefig(os.path.join(output_dir, f"tree_{i+1}.png"), dpi=300)
    plt.close()  # Close the figure after saving

cost_of_trees = optimiseur.display_cost_trees(search_space)

print(cost_of_trees)
