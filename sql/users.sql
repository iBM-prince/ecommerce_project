-- CREATION ET GESTIONS DES UTILAISATEURS --

-- CREATION DES INDEX POUR UNE MEILLEURE GESTION DES REQUETES

create index idx_pat_nom on patients(nom_pat);

create index idx_rdv_date on rendez_vous(date_rdv);

create index idx_utilisateur_role on utilisateurs(role);

-- CREATION DES UTILISATEURS --

create user 'admin_hopital'@'localhost' IDENTIFIED BY 'admin221';

create user 'medecin_user'@'localhost' identified by 'medecin221';

create user 'agent_user'@'localhost' identified by 'agent221';
    