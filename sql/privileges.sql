-- GESTIONS DES DROITS POUR LES DIFFERENTS UTILISATEURS --


-- DROITS POUR L'ADMINISTRATEUR --
grant all privileges on hopital_db.* to 'admin_hopital'@'localhost';

show grants for 'admin_hopital'@'localhost';

-- DROITS POUR LE MEDECIN --
grant select,insert on hopital_db.* to 'medecin_user'@'localhost';

revoke update,delete,create,drop on hopital_db.* from 'medecin_user'@'localhost';

show grants for 'medecin_user'@'localhost';

-- DROITS POUR L'AGENT --
grant select on hopital_db.* to 'agent_user'@'localhost';

revoke insert,update,delete,create,drop on hopital_db.* from 'agent_user'@'localhost';

show grants for 'agent_user'@'localhost';