-- GESTION DES DROITS POUR LES DIFFERENTS UTILISATEURS --

-- DROITS POUR L'ADMINISTRATEUR --
GRANT ALL PRIVILEGES ON hopital_db.* TO 'admin_hopital'@'localhost';
SHOW GRANTS FOR 'admin_hopital'@'localhost';

-- DROITS POUR LE MEDECIN --
GRANT SELECT, INSERT ON hopital_db.* TO 'medecin_user'@'localhost';
REVOKE UPDATE, DELETE, CREATE, DROP ON hopital_db.* FROM 'medecin_user'@'localhost';
SHOW GRANTS FOR 'medecin_user'@'localhost';

-- DROITS POUR L'AGENT --
GRANT SELECT ON hopital_db.* TO 'agent_user'@'localhost';
REVOKE INSERT, UPDATE, DELETE, CREATE, DROP ON hopital_db.* FROM 'agent_user'@'localhost';
SHOW GRANTS FOR 'agent_user'@'localhost';
