# DevOps S8 - TP2 Ansible

## Description

Ce projet a été réalisé dans le cadre du cours DevOps S8. Il automatise le déploiement complet d'une stack applicative sur une infrastructure gérée par Ansible. La stack est composée d'une API REST Node.js/Express, d'une base de données MySQL et d'un reverse proxy Nginx.

L'API expose deux endpoints :
- GET / : retourne un message de bienvenue en JSON
- GET /health : retourne le statut de l'application

## Stack technique

- Runtime : Node.js 20 + Express
- Base de données : MySQL
- Serveur web : Nginx (reverse proxy)
- Tests : Molecule + Testinfra
- Conteneur de test : Docker avec image geerlingguy/docker-ubuntu2404-ansible

## Prérequis

- Python 3.12+
- Docker
- Ansible

## Installation et lancement

1. Activer le virtualenv Python :
    source venv.sh

2. Installer les dépendances Python (Ansible, Molecule...) :
    rebuild_env

3. Installer les roles Ansible Galaxy :
    download_galaxy

4. Lancer les tests complets avec Molecule :
    molecule test

## Lancer l'application manuellement

    cd /opt/devops-api
    npm install
    node app.js
    L'API est accessible sur http://localhost:3000

## Structure du projet

    efrei-ansible-devops/
    roles/
        runtime/     # Installation de Node.js 20 via nodesource
        app/         # Déploiement de l'API Express + service systemd
        webserver/   # Configuration nginx avec template Jinja2
        database/    # Installation et démarrage de MySQL
    group_vars/
        all.yml      # Variables globales (config nginx, ports...)
    hosts/
        hosts_dev    # Inventaire avec groupes api, nginx, database
    molecule/
        default/
            molecule.yml      # Configuration Docker
            tests/test_app.py # Tests Testinfra
    playbook_install.yml  # Playbook principal

## Ce que j'ai fait étape par étape

### Étape 1 : Mise en place de l'environnement

Le projet de base utilise Vagrant + VirtualBox comme driver Molecule. Sur Windows avec WSL2, la configuration de VirtualBox nécessite beaucoup de paramétrage (plugin virtualbox_WSL2, variables VAGRANT_WSL_ENABLE_WINDOWS_ACCESS, PATH...). J'ai donc décidé de migrer vers Docker qui est plus simple à utiliser dans WSL2.

J'ai installé Docker dans WSL2 et modifié le fichier molecule/default/molecule.yml pour utiliser le driver Docker avec l'image geerlingguy/docker-ubuntu2404-ansible qui est une image Ubuntu 24.04 préconfigurée pour Ansible avec systemd.

### Étape 2 : Prise en main de Molecule

J'ai activé le virtualenv avec source venv.sh, installé les dépendances avec rebuild_env et les roles Galaxy avec download_galaxy. J'ai ensuite lancé molecule test pour vérifier que l'environnement fonctionnait correctement.

### Étape 3 : Création des roles Ansible

J'ai créé 4 roles :

- runtime : installe Node.js 20 via le dépôt officiel nodesource
- app : copie les fichiers de l'application (app.js, package.json), installe les dépendances npm et crée un service systemd pour démarrer l'API automatiquement
- webserver : configure nginx comme reverse proxy vers l'API avec un template Jinja2 pour rendre la configuration dynamique (port, hostname)
- database : installe MySQL et démarre le service

### Étape 4 : Tests Testinfra

J'ai écrit 6 tests dans molecule/default/tests/test_app.py pour vérifier que :
- nginx est installé, démarré et écoute sur le port 80
- MySQL est installé et démarré
- Node.js est bien installé
- Le service devops-api est démarré et écoute sur le port 3000

## Problèmes rencontrés et solutions

### 1. Migration Vagrant vers Docker
Le projet de base utilise Vagrant + VirtualBox. La configuration sur Windows WSL2 est très complexe et nécessite l'installation du plugin virtualbox_WSL2 ainsi que plusieurs variables d'environnement dans le .bashrc. Pour simplifier, j'ai migré vers Docker en modifiant le molecule.yml pour utiliser le driver Docker avec l'image geerlingguy/docker-ubuntu2404-ansible.

### 2. Paquet dirmngr manquant
Lors du premier molecule converge, le role geerlingguy.nginx échouait avec l'erreur "No package matching dirmngr is available". Ce paquet est nécessaire pour ajouter le dépôt apt officiel de nginx. Il n'était pas disponible par défaut dans le container Docker.
Solution : ajout d'une pre_task dans le playbook pour installer dirmngr avant d'exécuter le role nginx. J'ai aussi ajouté nginx_ppa_use: false dans group_vars/all.yml pour désactiver l'ajout du dépôt officiel nginx et utiliser la version des dépôts Ubuntu.

### 3. Problème d'idempotence sur NodeJS repository
Le test d'idempotence de molecule test échouait sur la task "Add NodeJS repository". Cette task utilise un script shell curl pour ajouter le dépôt nodesource, et Ansible la considérait comme "changed" à chaque exécution même si le dépôt était déjà installé.
Solution : ajout de changed_when: false sur la task pour indiquer à Ansible qu'elle ne modifie pas l'état du système si le fichier /etc/apt/sources.list.d/nodesource.list existe déjà.

### 4. Erreur d'indentation YAML dans molecule.yml
Lors des modifications du fichier molecule.yml avec nano, des erreurs d'indentation causaient des erreurs de parsing YAML au lancement de Molecule avec le message "mapping values are not allowed here".
Solution : réécriture complète du fichier avec la commande cat > fichier << EOF pour éviter les problèmes de copier-coller dans nano.


