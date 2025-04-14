--
-- Arquivo gerado com SQLiteStudio v3.4.8 em sex jan 3 07:48:18 2025
--
-- Codificação de texto usada: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Tabela: control_acess_entidade
CREATE TABLE control_acess_entidade (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, nome varchar (100) NOT NULL, status bool NOT NULL, tipo varchar (4) NOT NULL, cnpj varchar (14), email varchar (100), telefone varchar (11), endereco varchar (100), cep varchar (8), data_criacao datetime NOT NULL, data_modificacao datetime, cidade_id bigint REFERENCES control_acess_cidade (id) DEFERRABLE INITIALLY DEFERRED);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (1, 'PREFEITURA DE MIRANDA', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 18:15:19.214169', '2025-01-03 11:46:06', 51);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (2, 'PM CARACOL', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 21);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (3, 'FUNDO MUNICIPAL SAÚDE DE RIO NEGRO', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 66);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (4, 'PM CARACOL', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 21);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (5, 'PM CORGUINHO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 24);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (6, 'PM FIGUEIRÃO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (7, 'PM LADARIO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 48);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (8, 'PM RIO NEGRO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 66);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (9, 'PM ROCHEDO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 68);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (10, 'PM TERENOS', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 77);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (11, 'PM BANDEIRANTES', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 11);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (12, 'CM CARACOL', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 21);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (13, 'CM FIGUEIRÃO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (14, 'CM LADARIO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 48);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (15, 'CM CORGUINHO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 24);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (16, 'CM SELVIRIA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (17, 'CM PEDRO GOMES', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 61);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (18, 'CM RIO NEGRO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 66);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (19, 'CM TERENOS', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 77);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (20, 'CM BANDEIRANTES', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 11);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (21, 'CM MIRANDA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 51);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (22, 'CM CORUMBA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 26);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (23, 'QUALITY SISTEMAS', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (24, 'CM ROCHEDO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 68);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (25, 'INST. DE APOS. E PENSÕES DOS SERVIDORES MUN. DE TERENOS', 1, 'RPPS', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 77);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (26, 'PM ANTONIO JOÃO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (27, 'CM ANTONIO JOAO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 7);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (28, 'CM BODOQUENA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 15);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (29, 'ESCOLA MUNICIPAL JOÃO JOSÉ LEITE', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (30, 'CENTRO DE EDUCAÇÃO INFANTIL CRIANÇA FELIZ', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (31, 'CM NIOAQUE', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 54);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (32, 'HOSPITAL MUNICIPAL RITA ANTONIA MACIEL GODOY', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (33, 'CM DOIS IRMAOS DO BURITI', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 30);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (34, 'SERVIÇO AUTÔNOMO DE ÁGUA E ESGOTO DE CORGUINHO', 1, 'SAAE', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 24);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (35, 'CM RIO VERDE DE MATO GROSSO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 67);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (36, 'CM APARECIDA DO TABOADO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 8);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (37, 'CM GUIA LOPES DA LAGUNA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 37);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (38, 'CM CAMAPUA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 19);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (39, 'PM NIOAQUE', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 54);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (40, 'CM AGUA CLARA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (41, 'PM PARAISO DAS AGUAS', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (42, 'INSTITUTO MUNICIPAL DE PREVIDENCIA SOCIAL DE ROCHEDO', 1, 'RPPS', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 68);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (43, 'CM INOCENCIA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 39);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (44, 'CM PARAISO DAS AGUAS', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (45, 'CM COTRIGUACU', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (46, 'SECRETARIA MUNICIPAL DE SAUDE RIO NEGRO', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 66);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (47, 'FUNDO MUNICIPAL SAÚDE DE RIO NEGRO', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 66);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (48, 'INSTITUTO MUNICIPAL DE PREVIDENCIA SOCIAL DE LADARIO', 1, 'RPPS', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 48);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (49, 'CM NOVO HORIZONTE DO SUL', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 57);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (50, 'CM ARAL MOREIRA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 10);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (51, 'CM NOVA ALVORADA DO SUL', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 55);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (52, 'CM ANGELICA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (53, 'PM QUALITY SISTEMAS', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (54, 'SERVICO AUTONOMO DE AGUA E ESGOTO DE PARAISO DAS AGUAS-SAAE', 1, 'SAAE', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (55, 'CM DEODAPOLIS', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 29);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (56, 'INST. MUN. DE PREV. SOCIAL DOS SERV. DE ANTONIO JOAO-IMPS', 1, 'RPPS', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 7);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (57, 'PMCAMAPUA', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 19);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (58, 'CM JARDIM', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 45);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (59, 'CM PORTO MURTINHO', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 63);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (60, 'SERVICO AUTONOMO DE AGUA E ESGOTO DE BANDEIRANTES', 1, 'SAAE', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 11);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (61, 'SECRETARIA MUNICIPAL DE SAUDE DE CARACOL', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 21);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (62, 'ESF LIDIANE DE OLIVEIRA GARDIN GALEANO', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (63, 'ESF CANDELARIA NUNES', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (64, 'ESF IRIA CONCEICAO ALVARENGA MENDES', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (65, 'PLENUS CONSULTORIA', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (66, 'HOSPITAL E MATERNIDADE IDIMAQUE PAES FERREIRA', 1, 'O', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 1);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (67, 'PMNOVA ALVORADA DO SUL', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 55);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (68, 'CM BELA VISTA', 1, 'C', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 14);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (69, 'PM INOCENCIA', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 39);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (70, 'PM MUNICIPAL PORTO MURTINHO', 1, 'P', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 63);
INSERT INTO control_acess_entidade (id, nome, status, tipo, cnpj, email, telefone, endereco, cep, data_criacao, data_modificacao, cidade_id) VALUES (71, 'INST. DE PREV DOS SERV. PUBLICOS DO PMCAMAPUA', 1, 'RPPS', '0', 'teste@teste.gmail', '0', 'rua das flores', '79000000', '2025-01-02 20:28:58', '2025-01-03 11:46:06', 19);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
