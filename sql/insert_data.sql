-- CHARGEMENT DONNEES UTILISATEURS --

 LOAD DATA LOCAL INFILE 'C:/Users/torre/ecommerce_project/sql/csv/utilisateurs.csv' 
            INTO TABLE utilisateurs FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' IGNORE 1 ROWS (nom, prenom, email, mot_de_passe, role);

-- CHARGEMENT DONNEES PATIENTS --
 LOAD DATA LOCAL INFILE 'C:/Users/torre/ecommerce_project/sql/csv/patients.csv' 
            INTO TABLE patients FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' IGNORE 1 ROWS (nom_pat, prenom_pat, date_naissance, sexe, telephone);

-- CHARGEMENT DONNEES MEDECINS --
 LOAD DATA LOCAL INFILE 'C:/Users/torre/ecommerce_project/sql/csv/medecins.csv' 
            INTO TABLE medecins FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' IGNORE 1 ROWS (nom_med, prenom_med, specialite, id_user);

-- CHARGEMENT DONNEES RENDEZ_VOUS --
 LOAD DATA LOCAL INFILE 'C:/Users/torre/ecommerce_project/sql/csv/rendez_vous.csv' 
            INTO TABLE rendez_vous FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' IGNORE 1 ROWS (date_rdv, id_pat, id_med);

-- CHARGEMENT DONNEES HOSPITALISATIONS --
 LOAD DATA LOCAL INFILE 'C:/Users/torre/ecommerce_project/sql/csv/hospitalisations.csv' 
            INTO TABLE hospitalisations FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' IGNORE 1 ROWS (date_entree, date_sortie, id_pat);

-- CHARGEMENT DONNEES TRAITEMENTS --
 LOAD DATA LOCAL INFILE 'C:/Users/torre/ecommerce_project/sql/csv/traitements.csv' 
            INTO TABLE traitements FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
            LINES TERMINATED BY '\n' IGNORE 1 ROWS (description, date_traitement, id_pat);
