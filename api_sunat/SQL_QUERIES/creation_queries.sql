-- Create tables with DNI as the primary key
CREATE TABLE Personas (
    dni VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(255),
    fecha_nacimiento DATE,
    estado_civil VARCHAR(20),
    dependientes INT
);

CREATE TABLE Ingresos (
    ingreso_id SERIAL PRIMARY KEY,
    dni_persona VARCHAR(10) REFERENCES Personas(dni),
    ingresos_brutos_totales DECIMAL(10, 2),
    otros_ingresos JSONB
);

CREATE TABLE Deducciones (
    deduccion_id SERIAL PRIMARY KEY,
    dni_persona VARCHAR(10) REFERENCES Personas(dni),
    gastos_educativos DECIMAL(10, 2),
    donaciones_caritativas DECIMAL(10, 2)
);

CREATE TABLE CreditosFiscales (
    credito_id SERIAL PRIMARY KEY,
    dni_persona VARCHAR(10) REFERENCES Personas(dni),
    credito_por_hijos DECIMAL(10, 2)
);

CREATE TABLE Retenciones (
    retencion_id SERIAL PRIMARY KEY,
    dni_persona VARCHAR(10) REFERENCES Personas(dni),
    impuesto_renta_retenido DECIMAL(10, 2),
    contribucion_seguridad_social_retenida DECIMAL(10, 2)
);

-- Insertar datos en la tabla "Personas"
INSERT INTO Personas (dni, nombre, fecha_nacimiento, estado_civil, dependientes)
VALUES
    ('12345678', 'Juan Pérez', '1990-01-15', 'Soltero', 2),
    ('23456789', 'Ana García', '1985-05-20', 'Casado', 1),
    ('34567890', 'Pedro Rodríguez', '1978-09-10', 'Soltero', 0),
    ('45678901', 'María Torres', '1992-03-25', 'Casado', 3),
    ('56789012', 'Luisa Mendoza', '1980-12-08', 'Soltero', 0),
    ('67890123', 'Carlos Vargas', '1973-07-17', 'Casado', 2),
    ('78901234', 'Sofía López', '1988-11-30', 'Casado', 1),
    ('89012345', 'Eduardo Gómez', '1995-04-03', 'Soltero', 0),
    ('90123456', 'Luis García', '1987-08-22', 'Soltero', 1),
    ('01234567', 'Laura Martínez', '1993-06-14', 'Casado', 2);

-- Insertar datos en la tabla "Ingresos"
INSERT INTO Ingresos (dni_persona, ingresos_brutos_totales, otros_ingresos)
VALUES
    ('12345678', 5000.00, '{"alquileres": 200.00, "intereses_bancarios": 50.00}'),
    ('23456789', 6000.00, '{"alquileres": 300.00, "intereses_bancarios": 70.00}'),
    ('34567890', 4500.00, '{"alquileres": 150.00, "intereses_bancarios": 30.00}'),
    ('45678901', 7000.00, '{"alquileres": 250.00, "intereses_bancarios": 60.00}'),
    ('56789012', 5500.00, '{"alquileres": 180.00, "intereses_bancarios": 40.00}'),
    ('67890123', 8000.00, '{"alquileres": 350.00, "intereses_bancarios": 80.00}'),
    ('78901234', 6200.00, '{"alquileres": 280.00, "intereses_bancarios": 65.00}'),
    ('89012345', 5200.00, '{"alquileres": 170.00, "intereses_bancarios": 35.00}'),
    ('90123456', 4800.00, '{"alquileres": 120.00, "intereses_bancarios": 25.00}'),
    ('01234567', 7500.00, '{"alquileres": 300.00, "intereses_bancarios": 70.00}');

-- Insertar datos en la tabla "Deducciones"
INSERT INTO Deducciones (dni_persona, gastos_educativos, donaciones_caritativas)
VALUES
    ('12345678', 300.00, 50.00),
    ('23456789', 250.00, 40.00),
    ('34567890', 200.00, 30.00),
    ('45678901', 350.00, 60.00),
    ('56789012', 280.00, 50.00),
    ('67890123', 400.00, 70.00),
    ('78901234', 300.00, 45.00),
    ('89012345', 220.00, 35.00),
    ('90123456', 180.00, 30.00),
    ('01234567', 400.00, 75.00);

-- Insertar datos en la tabla "CreditosFiscales"
INSERT INTO CreditosFiscales (dni_persona, credito_por_hijos)
VALUES
    ('12345678', 100.00),
    ('23456789', 80.00),
    ('34567890', 60.00),
    ('45678901', 120.00),
    ('56789012', 90.00),
    ('67890123', 150.00),
    ('78901234', 110.00),
    ('89012345', 70.00),
    ('90123456', 50.00),
    ('01234567', 130.00);

-- Insertar datos en la tabla "Retenciones"
INSERT INTO Retenciones (dni_persona, impuesto_renta_retenido, contribucion_seguridad_social_retenida)
VALUES
    ('12345678', 800.00, 200.00),
    ('23456789', 900.00, 180.00),
    ('34567890', 700.00, 160.00),
    ('45678901', 1000.00, 220.00),
    ('56789012', 850.00, 190.00),
    ('67890123', 1100.00, 240.00),
    ('78901234', 920.00, 200.00),
    ('89012345', 780.00, 170.00),
    ('90123456', 660.00, 150.00),
    ('01234567', 1050.00, 230.00);
