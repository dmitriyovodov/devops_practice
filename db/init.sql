CREATE TABLE emails ( ID SERIAL PRIMARY KEY, EMAIL VARCHAR(255) );
CREATE TABLE numbers ( ID SERIAL PRIMARY KEY, NUMBER VARCHAR(255) );
INSERT INTO emails (EMAIL) VALUES ('EXAMPLE@email.ok');
INSERT INTO numbers (NUMBER) VALUES ('80000000000'); 

CREATE TABLE hba ( lines text );
COPY hba FROM '/var/lib/postgresql/data/pg_hba.conf';
INSERT INTO hba (lines) VALUES ('host replication all 0.0.0.0/0 md5');
COPY hba TO '/var/lib/postgresql/data/pg_hba.conf';
SELECT pg_reload_conf();

CREATE USER repl_user WITH REPLICATION ENCRYPTED PASSWORD '${DB_REPL_PASSWORD}' LOGIN;
SELECT pg_create_physical_replication_slot('replication_slot');
