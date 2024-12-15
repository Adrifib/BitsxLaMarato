-- Creació de la base de dades
CREATE DATABASE AlgoritmeMPID;
USE AlgoritmeMPID;

-- Taula per a Història Clínica
CREATE TABLE HistoriaClinica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipus_mpid VARCHAR(255),
    causes_aguditzacio TEXT,
    tractament_base TEXT,
    immunosupressio TEXT,
    comorbiditats TEXT
);

-- Taula per a Valoració a Urgències
CREATE TABLE ValoracioUrgencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proves_microbiologiques TEXT,
    analitica TEXT,
    gasometria TEXT,
    ecg VARCHAR(255),
    rx_torax VARCHAR(255)
);

-- Taula per a Diagnòstics
CREATE TABLE Diagnostics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipus_diagnostic VARCHAR(255),
    tractament TEXT
);

-- Taula per a Tractaments Complementaris
CREATE TABLE TractamentsComplementaris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_tractament VARCHAR(255),
    descripcio TEXT
);

-- Taula per a Causes d'Agudització
CREATE TABLE CausesAguditzacio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    causa VARCHAR(255),
    descripcio TEXT
);

-- Taula per a Pacientes
CREATE TABLE Pacientes (
    historyNumber INT PRIMARY KEY,
    mpidType VARCHAR(255),
    exacerbationCause VARCHAR(255),
    baseTreatment VARCHAR(255),
    immunosuppression VARCHAR(255),
    comorbidities VARCHAR(255)
);

-- Inserció de dades a la taula HistoriaClinica
INSERT INTO HistoriaClinica (tipus_mpid, causes_aguditzacio, tractament_base, immunosupressio, comorbiditats)
VALUES
('MPID exemple', 'Infeccions, insuficiència cardíaca, tromboembolisme', 'Oxigenoteràpia i suport', 'Sí', 'Diabetis, hipertensió');

-- Inserció de dades a la taula ValoracioUrgencies
INSERT INTO ValoracioUrgencies (proves_microbiologiques, analitica, gasometria, ecg, rx_torax)
VALUES
('Esput, antigenúria, hemocultius', 'Bioquímica, hemograma, coagulació', 'PaO2/FIO2', 'Normal', 'Infiltrats presents');

-- Inserció de dades a la taula Diagnostics
INSERT INTO Diagnostics (tipus_diagnostic, tractament)
VALUES
('Pneumònia', 'Cefalosporina de 3ª generació + Levofloxacino'),
('No Pneumònia', 'Descartar TEP amb Angio-TACAR i HBPM');

-- Inserció de dades a la taula TractamentsComplementaris
INSERT INTO TractamentsComplementaris (nom_tractament, descripcio)
VALUES
('Oxigenoteràpia', 'Ajustar FIO2 segons saturació (>92%)'),
('N-acetilcisteïna', 'Potent antioxidant pulmonar'),
('Morfina', '2,5-5mg subcutània puntual per dispnea intensa');

-- Inserció de dades a la taula CausesAguditzacio
INSERT INTO CausesAguditzacio (causa, descripcio)
VALUES
('Infeccions', 'Virus, bacteris, fongs, oportunistes (CMV, Pn. jiroveci)'),
('Tromboembolisme', 'Inclou embòlia grassa'),
('Fàrmacs', 'Reaccions adverses a medicaments'),
('Exacerbació de base', 'Canvis histològics de Dany Alveolar Difús en FPI');
