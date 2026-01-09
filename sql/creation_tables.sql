-- CREATION DE LA BASE DE DONNEES HOPITAL_DB --

CREATE DATABASE hopital_db;

-- UTILISATION DE LA BASE DE DONNEES HOPITAL_DB --

USE hopital_db;
-- CREATION DE LA TABLE UTILISATEURS --

create table utilisateurs(id_user int auto_increment primary key,
            nom varchar(100) not null, prenom varchar(100) not null, 
            email varchar(100) unique not null, mot_de_passe varchar(100) not null, 
            role enum('admin','medecin','agent') not null);

-- CREATION DE LA TABLE PATIENTS --

create table patients(id_pat int auto_increment primary key, 
            nom_pat varchar(100) not null, prenom_pat varchar(100) not null, 
            date_naissance date not null,sexe enum('m','f') ,telephone int not null);

-- CREATION DE LA TABLE MEDECINS --

create table medecins(id_med int auto_increment primary key, 
            nom_med varchar(100) not null, prenom_med varchar(100) not null, 
            specialite varchar(100) not null, id_user int , 
            foreign key(id_user) references utilisateurs(id_user));

-- CREATION DE LA TABLE RENDEZ_VOUS --

 create table rendez_vous(id_rdv int auto_increment primary key,
            date_rdv date not null,id_pat int not null,id_med int not null, 
            foreign key(id_pat) references patients(id_pat), 
            foreign key(id_med) references medecins(id_med));

-- CREATION DE LA TABLE HOSPITALISATION --

create table hospitalisations(id_hospi int auto_increment primary key, 
            date_entree date not null,date_sortie date, id_pat int not null, 
            foreign key(id_pat) references patients(id_pat));

-- CREATION DE LA TABLE TRAITEMENTS --

create table traitements(id_trait int auto_increment primary key,
            description text not null, date_traitement date not null,
            id_pat int not null, foreign key(id_pat) references patients(id_pat));