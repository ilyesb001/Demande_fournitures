# Demande_fournitures

Création du module demande fourniture:

    • La demande de fourniture est un document pour les employées pour qu’ils puissent faire des demandes de besoins (Bureautique, consommable, …etc)
    • La demande sera aprés sois validée soit refusé par le résponsable.
    • Dans le cas ou la demande est validé par le résponsable elle passe au gestionnaire de stock.
    • Si les articles dans la demande sont disponible, le GDS va valider la demande.
    • Lors de la validation, la demande sera terminé.
    • Dans le cas d’un refus, une convention d’achats sera créé pour demander l’achats de nouvelles articles.
    • La demande peut étre terminé seuelement si les bons de commande de la convention d’achat (sorties) sont fait.

    1. Créer un nouveau module demande fourniture.
    2. Dépend sur le module “base”, “achats” et “hr”.
    3. Créer un menu niveau module (top level) avec icon qui ouvre une vue kanban, list et formulaire.
    4. Le model demande fourniture a les champs suivants:
        ◦ Nom (référence).
        ◦ État : pour les différentes étapes de la demande (Brouillon, annulé, fait, etc)
        ◦ Demandeur (employé) et son poste, sa structure (direction),  Son responsible (voir module hr).
        ◦ Un champ pour la société.
        ◦ Un champ pour les catégories d’articles .
        ◦ Date de demande, date de validation, date de fin (fermeture ou annulation)
        ◦ Un champ pour les lignes des articles qui contient :
            ▪ L’article
            ▪ Quantité demandé
            ▪ Type d’opération ( voir module stock)
            ▪ Ajoutez d’autre champs si necessaire
        ◦ Ajoutez d’autre champs si necessaire
    5. Les champs demandeur, catégories, sont obligatoires
    6. Rendre les champs neccesaire non modifiable (readonly) si necessaire
    7. Ajoutez les boutons adéquats pour passer d’un état à l’autre en implémentat la logique necessaire sans oublier la validation des champs et informations saisie si nécessaire
    8. Seule le responsible du demandeur peut valider ou refuser la demande 
    9. Seule le GDS peut valider ou refuser la demande aprés la validation du responsible (meme le responsible ne peut pas valider au lieu du GDS)
    10. Envoyer un message en privé + email au demandeur quand la demande est validé par GDS
    11. La demande peut etre annulée seulement a l’état brouillon
    12. La demande peut etre supprimé a l’état brouilon ou annulé
    13. Le demandeur peut voir seulement ses demandes
    14. Le responsible peut voir les demandes de ses éléments (employés qu’il controle) et ses propres demandes
    15. Le GDS peut voir seulement les demandes validés par le responsible
    16. Un administrateur peut voir toutes les demandes
    17. Ajouter Un état d’impression (report) en interne pour la demande de fourniture

NB:
    • Travaillez avec GIT si possible.
    • Essaiez de bien structurer votre code, utiliser des noms significatifs et claires pour les champs, les modeles, …..
    • Commentez votre code si nécessaire.
    • Ajoutez des modèles et vues que vous trouvez utiles et/ou nécessaires
    • Éssaiez de travailer avec toutes les aquis de odoo (Model, Vues, Rapports, Wizards, Différentes types de champs).
    • Des fonctinnalités supplémentaires implémentés sont les bienvenus.
