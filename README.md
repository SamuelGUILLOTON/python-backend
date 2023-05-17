# PYTHON_BACKEN
Ceci est application fait dans le cadre du cours de python d'efficom. Elle permet à des entreprises et des utilisateurs de gérer leur planning. 

## Getting started
installation sans docker.
pour installer les dépendances: pip install -r requirements.txt
pour lancer le serveur : python -m uvicorn main:app --reload
et go to http://localhost:8000/doc 

# Database information
![image bdd]([https://i.ibb.co/5c2vn6L/nom-de-l-image.jpg](https://i.imgur.com/KP34FGN.png)

# Table USER

| id | lastname_hash | firstname_hash | mail_hash                | company_id | role       | password_hash  |
|----|---------------|----------------|--------------------------|------------|------------|-----------|
| 31 | Réno          | Jean           | jean-réno@mail.com       | 2          | MAINTAINER | password  |
| 32 | Céline        | Dion           | céline-dion@mail.com     | 3          | MAINTAINER | password  |
| 34 | Brad          | Pitt           | brad-pitt@mail.com       | 5          | ADMIN      | password  |
| 35 | Brad          | Pitt           | brad-cscdcssdcpitt@mail.com | 3        | ADMIN      | password  |
| 37 | Al            | Pacino         | al-pacino@mail.com       | 2          | USER       | password  |
| 38 | pierre        | eastwood       | clint-eastwood@mail.com  | 3          | USER       | password3  |

# Table Company

Voici le tableau Markdown basé sur les données fournies :

| id | name    | address              | siret     | owner_id |
|----|---------|----------------------|-----------|----------|
| 2  | OOUIGO  | 6 rue andré malraux  | 43455     | 31       |
| 3  | Flixbus | 3 rue de chez moi    | 454543534 | 32       |
| 5  | CORA    | 5 rue André          | 3223      | 34       |

# Table Planning

| id | planning              | company_id | created_at           | updated_at           | start_date            | end_date              |
|----|-----------------------|------------|----------------------|----------------------|-----------------------|-----------------------|
| 1  | SERVICE IT            | 2          | 2023-05-12 21:52:42  | 2023-05-12 21:52:42  | 2023-05-12 21:52:42   | 2023-05-12 21:52:42   |
| 2  | SERVICE WEB           | 3          | 2023-05-12 21:52:42  | 2023-05-12 21:52:42  | 2023-05-12 21:52:42   | 2023-05-12 21:52:42   |
| 3  | Service communication | 5          | 2023-05-17 11:37:58  | 2023-05-17 11:37:58  | 2023-05-17 11:37:58   | 2023-05-17 11:37:58   |
| 4  | Servcie Cantine       | 5          | 2023-05-17 11:37:58  | 2023-05-17 11:37:58  | 2023-05-17 11:37:58   | 2023-05-17 11:37:58   |
| 5  | Equipe de Tennis      | 2          | 2023-05-17 11:40:10  | 2023-05-17 11:40:10  | 2023-05-17 11:40:10   | 2023-05-17 11:40:10   |
| 6  | Service Commerce      | 3          | 2023-05-17 11:40:10  | 2023-05-17 11:40:10  | 2023-05-17 11:40:10   | 2023-05-17 11:40:10   |

# Table Activité

| id | activity   | start_date         | end_date           | owner_id | planning_id | created_at       |
|----|------------|--------------------|--------------------|----------|-------------|------------------|
| 1  | sport      | 2023-05-17 08:32:02 | 2023-05-17 08:32:02 | 31       | 2           | 2023-05-12 22:03:21 |
| 2  | formation  | 2023-05-12 22:03:21 | 2023-05-12 22:03:21 | 31       | 2           | 2023-05-12 22:03:21 |
| 3  | jeux vidéo | 2023-05-17 08:32:02 | 2023-05-17 08:32:02 | 32       | 1           | 2023-05-12 22:03:21 |

# Table Notification

Voici un tableau Markdown rapide basé sur les données fournies :

| id | created_at         | activity_id | message                                |
|----|--------------------|-------------|----------------------------------------|
| 1  | 2023-05-17 10:32:43 | 1           | there is some change on your activity, jeux vidéo |
| 2  | 2023-05-17 10:33:14 | 3           | there is some change on your activity, jeux vidéo |
| 3  | 2023-05-17 10:34:17 | 3           | there is some change on your activity, jeux vidéo |
| 4  | 2023-05-17 10:34:23 | 1           | there is some change on your activity, jeux vidéo |

# Table userActivity

| id | activity_id | user_id |
|----|-------------|---------|
| 4  | 1           | 24      |
| 2  | 2           | 1       |
| 8  | 3           | 34      |
| 6  | 3           | 35      |
| 5  | 3           | 38      |

# Grille d'évaluation du projet en utilisant FastAPI

## 1. Structure du projet et organisation du code (35 points)
   - [x] README.md clair et bien documenté (sachant qu'un README ne me permettant pas d'exécuter le code entraînera une réduction de la note globale de 33%) (5 points)
   - [x] Organisation des fichiers et dossiers (5 points)
   - [x] Utilisation appropriée des modules et packages (5 points)
   - [x] Lisibilité et propreté du code (10 points)
   - [x] Commentaires lisibles et faisant sens (5 points)
   - [x] Bonne utilisation du git (commits de bonne taille, messages faisant sens) (5 points)

## 2. Implémentation des standards appris en cours (35 points)
   - [x] Utilisation de pydantic (5 points)
   - [x] Section d'import bien formatée (system, libs, local), et chemins absolus et non relatifs. Requirements.py avec versions fixes (5 points)
   - [x] Définition du type de donnée en retour des fonctions. (5 points)
   - [x] Bonne utilisation des path & query parameters (10 points)
   - [x] Retour des bons codes HTTP (10 points)

## 3. Implémentation des fonctionnalités demandées (85 points)
   - [x] Connexion à la base de données (30 points)
   - [x] Gestion des utilisateurs (15 points)
   - [x] Gestion des plannings (15 points)
   - [x] Gestion des activités (15 points)
   - [x] Gestion des entreprises (10 points)

## 4. Sécurité (20 points)
   - [x] Utilisation de tokens pour l'authentification (JWT) (5 points)
   - [x] Validation et vérification des données entrantes avec modèles pydantics, not (5 points)
   - [x] Gestion des erreurs et exceptions (5 points)
   - [x] Sécurisation de la connexion à la base de données (5 points)
