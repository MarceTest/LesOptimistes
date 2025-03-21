Contenu du depot :

Notebook : query_sampling_for_Estimating_local_cost_final.ipynb
 	
	-> Processus d'estimation des paramètres de la fonction de coût.

Prototype : main.py optimizer.py parser.py search_spacer.py cost_model.py catalog.py _more.py
	
	-> Entrée : Requête et sa classe
	-> Sortie : 3 plans alternatifs dans un dossier "trees" et le coût de chacun des arbre dans le terminal 

	-> exemple d'exécution : python main.py "SELECT ANNEE FROM TB1, TAB2 WHERE ANNEE = '2021'" 3

NB : Le prototype à été simplifié pour la démonstration de soutenance afin de ne gérer que les requêtes faites sur les attributs DEPT, REGION et ANNEE. Les tables peuvent être des intitulés quelconques. Les conditions ne peuvent être que des opération "=" et les attributs et les valeurs de la condition possibles sont disponibles dans les fichiers JSON du dossier json_files