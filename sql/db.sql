-- Eliminar base de datos si existe
DROP DATABASE IF EXISTS comics;

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS comics;
USE comics;

-- Crear tabla de Estados de Pedido
CREATE TABLE EstadosPedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(50) NOT NULL
);

-- Crear tabla de Clientes
CREATE TABLE Clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pedidos INT NOT NULL DEFAULT 0,
    cliente_frecuente BOOLEAN DEFAULT FALSE
);

-- Crear tabla de Categorías de Productos
CREATE TABLE Categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Crear tabla de Editoriales
CREATE TABLE Editoriales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Crear tabla de Proveedores
CREATE TABLE Proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL,
    direccion VARCHAR(255),
    fecha_ultimo_abastecimiento DATE NULL
);

-- Crear tabla de Productos
CREATE TABLE Productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    stock INT NOT NULL DEFAULT 0,
    precio DECIMAL(10,2) NOT NULL,
    categoria_id INT NOT NULL,
    editorial_id INT DEFAULT NULL,
    proveedor_id INT DEFAULT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(id),
    FOREIGN KEY (editorial_id) REFERENCES Editoriales(id),
    FOREIGN KEY (proveedor_id) REFERENCES Proveedores(id)
);

-- Crear tabla de Pedidos
CREATE TABLE Pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estado_id INT NOT NULL,
    fecha_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega TIMESTAMP NULL,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
    FOREIGN KEY (estado_id) REFERENCES EstadosPedidos(id)
);

-- Crear tabla de Detalles de Pedidos
CREATE TABLE DetallesPedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);

-- Crear tabla de Fechas de Abastecimiento
CREATE TABLE FechasAbastecimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    proveedor_id INT NOT NULL,
    fecha_abastecimiento DATETIME NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES Productos(id),
    FOREIGN KEY (proveedor_id) REFERENCES Proveedores(id)
);

-- Crear tabla de tipos de promociones
CREATE TABLE TiposPromociones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    detalle_promocion VARCHAR(10) NOT NULL
);

-- Crear tabla de promociones
CREATE TABLE Promociones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    promocion_id INT NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES Productos(id),
    FOREIGN KEY (promocion_id) REFERENCES TiposPromociones(id)
);

-- STORAGE PRODECURES

DELIMITER $$

-- Agregar un nuevo producto asegurando que la categoría, editorial y proveedor existen
CREATE PROCEDURE AgregarProducto(
    IN p_nombre VARCHAR(100),
    IN p_stock INT,
    IN p_precio DECIMAL(10,2),
    IN p_categoria_id INT,
    IN p_editorial_id INT,
    IN p_proveedor_id INT
)
BEGIN
    -- Verificar existencia de llaves foráneas antes de insertar
    IF EXISTS (SELECT 1 FROM Categorias WHERE id = p_categoria_id) AND
       EXISTS (SELECT 1 FROM Editoriales WHERE id = p_editorial_id) AND
       EXISTS (SELECT 1 FROM Proveedores WHERE id = p_proveedor_id) THEN
        INSERT INTO Productos (nombre, stock, precio, categoria_id, editorial_id, proveedor_id)
        VALUES (p_nombre, p_stock, p_precio, p_categoria_id, p_editorial_id, p_proveedor_id);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Una de las claves foráneas no existe';
    END IF;
END$$

-- Registrar un nuevo pedido y calcular el total
CREATE PROCEDURE RegistrarPedido(
    IN p_cliente_id INT,
    IN p_total DECIMAL(10,2),
    OUT p_pedido_id INT
)
BEGIN
    INSERT INTO Pedidos (cliente_id, total, estado_id)
    VALUES (p_cliente_id, p_total, 1); -- Estado 1 = "Pendiente"
    SET p_pedido_id = LAST_INSERT_ID();
END$$

-- Registrar un detalle de pedido asegurando stock suficiente
CREATE PROCEDURE AgregarDetallePedido(
    IN p_pedido_id INT,
    IN p_producto_id INT,
    IN p_cantidad INT
)
BEGIN
    DECLARE v_stock INT;
    
    SELECT stock INTO v_stock FROM Productos WHERE id = p_producto_id;

    IF v_stock >= p_cantidad THEN
        INSERT INTO DetallesPedidos (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (p_pedido_id, p_producto_id, p_cantidad, 
                (SELECT precio FROM Productos WHERE id = p_producto_id),
                p_cantidad * (SELECT precio FROM Productos WHERE id = p_producto_id));

        -- Actualizar stock
        UPDATE Productos SET stock = stock - p_cantidad WHERE id = p_producto_id;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Stock insuficiente';
    END IF;
END$$

-- Consultar historial de pedidos de un cliente
CREATE PROCEDURE HistorialPedidosCliente(IN p_cliente_id INT)
BEGIN
    SELECT p.id, p.total, ep.estado, p.fecha_pedido
    FROM Pedidos p
    INNER JOIN EstadosPedidos ep ON p.estado_id = ep.id
    WHERE p.cliente_id = p_cliente_id
    ORDER BY p.fecha_pedido DESC;
END$$


-- Actualizar el estado de un pedido
CREATE PROCEDURE ActualizarEstadoPedido(
    IN p_pedido_id INT,
    IN p_nuevo_estado_id INT
)
BEGIN
    UPDATE Pedidos SET estado_id = p_nuevo_estado_id WHERE id = p_pedido_id;
END$$

DELIMITER ;

-- TRIGGERS

DELIMITER //

CREATE TRIGGER aumentar_contador_de_pedidos
AFTER INSERT ON Pedidos
FOR EACH ROW
BEGIN
    UPDATE Clientes
    SET pedidos = pedidos + 1
    WHERE id = NEW.cliente_id;
END//

CREATE TRIGGER actualizar_total_de_pedido
AFTER INSERT ON DetallesPedidos
FOR EACH ROW
BEGIN
    UPDATE Pedidos
    SET total = total + NEW.subtotal
    WHERE id = NEW.pedido_id;
END//

CREATE TRIGGER actualizar_fecha_de_abastecimiento
AFTER INSERT ON FechasAbastecimiento
FOR EACH ROW
BEGIN
    UPDATE Proveedores
    SET fecha_ultimo_abastecimiento = NEW.fecha_abastecimiento
    WHERE id = NEW.proveedor_id;
END//

CREATE TRIGGER reducir_stock
AFTER INSERT ON DetallesPedidos
FOR EACH ROW
BEGIN
    UPDATE Productos
    SET stock = stock - NEW.cantidad
    WHERE id = NEW.producto_id;
END//

CREATE TRIGGER agregar_fecha_de_entrega_de_pedido
BEFORE INSERT ON Pedidos
FOR EACH ROW
BEGIN
    IF NEW.estado_id = 4 THEN
        SET NEW.fecha_entrega = CURRENT_TIMESTAMP;
    END IF;
END//

DELIMITER ;

-- Inserciones de datos

-- Insertar estados de pedido
INSERT INTO EstadosPedidos (estado) VALUES
('Pendiente'), ('En almacén'), ('Enviado'), ('Entregado'), ('Cancelado');

-- Insertar clientes con clientes frecuentes
INSERT INTO Clientes (nombre, email, telefono, direccion) VALUES
('Juan Pérez', 'juan.perez@example.com', '555-1234', 'Calle Falsa 123'),
('Ana López', 'ana.lopez@example.com', '555-5678', 'Av. Siempre Viva 742'),
('Carlos Méndez', 'carlos.mendez@example.com', '555-8765', 'Calle Principal 456'),
('María García', 'maria.garcia@example.com', '555-4321', 'Plaza Central 789'),
('Pedro Sánchez', 'pedro.sanchez@example.com', '555-1111', 'Boulevard del Sol 321'),
('Laura Jiménez', 'laura.jimenez@example.com', '555-2222', 'Paseo del Río 654'),
('Roberto Díaz', 'roberto.diaz@example.com', '555-3333', 'Avenida Libertad 987'),
('Sofía Castillo', 'sofia.castillo@example.com', '555-4444', 'Camino Real 147'),
('Diego Torres', 'diego.torres@example.com', '555-5555', 'Colina Verde 258'),
('Elena Ruiz', 'elena.ruiz@example.com', '555-6666', 'Cerro Azul 369');

-- Insertar categorías de productos
INSERT INTO Categorias (nombre) VALUES
('Figuras de Acción'),
('Merchandising'),
('Manga'),
('Novelas Gráficas'),
('Cómics Independientes'),
('Cómics Europeos'),
('Cómics de Terror'),
('Cómics de Ciencia Ficción'),
('Cómics de Fantasía'),
('Cómics Infantiles'),
('Cómics Clásicos');

-- Insertar editoriales de cómics
INSERT INTO Editoriales (nombre) VALUES
('Marvel Comics'),
('DC Comics'),
('Shueisha'),
('Kodansha'),
('Dark Horse Comics'),
('Image Comics'),
('VIZ Media'),
('Norma Editorial'),
('ECC Ediciones'),
('Planeta Cómic');

-- Insertar proveedores especializados
INSERT INTO Proveedores (nombre, telefono, email, direccion) VALUES
('Distribuidora Marvel', '555-0001', 'marvel@distribuidora.com', 'Av. Comic 100'),
('Distribuidora DC', '555-0002', 'dc@distribuidora.com', 'Calle Gotham 200'),
('Manga World', '555-0003', 'manga@world.com', 'Paseo Anime 300'),
('Comic Store', '555-0004', 'comics@store.com', 'Plaza Heroica 400'),
('Graphic Novels Inc.', '555-0005', 'novels@inc.com', 'Boulevard Creativo 500'),
('Indie Comics', '555-0006', 'indie@comics.com', 'Camino Alternativo 600'),
('Fantasy Supplies', '555-0007', 'fantasy@supplies.com', 'Calle Mágica 700'),
('Sci-Fi Distributions', '555-0008', 'scifi@distributions.com', 'Galaxia 800'),
('Kids Comics', '555-0009', 'kids@comics.com', 'Parque Infantil 900'),
('Classic Comics', '555-0010', 'classic@comics.com', 'Avenida Nostalgia 1000');


-- Insertar productos de cómics y figuras
INSERT INTO Productos (nombre, stock, precio, categoria_id, editorial_id, proveedor_id) VALUES
('Cómic: X-Men #5', 40, 8.99, 1, 1, 1),
('Cómic: Daredevil Born Again', 35, 10.50, 1, 1, 1),
('Cómic: Watchmen Edición Deluxe', 25, 18.75, 1, 2, 2),
('Cómic: Sandman Volumen 1', 20, 15.99, 1, 2, 2),
('Figura: Vegeta Blue', 18, 38.50, 2, 4, 3),
('Figura: Captain America Endgame', 12, 42.99, 2, 1, 1),
('Camiseta de Batman', 30, 21.99, 3, 2, 2),
('Camiseta de Flash', 28, 18.50, 3, 2, 2),
('Cómic: Hellboy Volumen 1', 22, 14.25, 1, 3, 3),
('Figura: Luffy Gear Fifth', 10, 50.00, 2, 4, 3);

-- Insertar pedidos con diferentes estados
INSERT INTO Pedidos (cliente_id, estado_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1),
(5, 2),
(6, 3),
(7, 1),
(8, 2),
(9, 3),
(10, 1);

-- Insertar detalles de pedidos
INSERT INTO DetallesPedidos (pedido_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(4, 2, 2, 12.50, 25.00),
(5, 5, 1, 19.99, 19.99),
(6, 1, 3, 9.99, 29.97),
(7, 3, 2, 35.99, 71.98),
(8, 4, 1, 45.99, 45.99),
(9, 2, 1, 12.50, 12.50),
(10, 5, 2, 19.99, 39.98),
(1, 5, 2, 19.99, 39.98),
(2, 4, 1, 45.99, 45.99),
(3, 2, 3, 12.50, 37.50);

-- Insertar fechas de abastecimiento
INSERT INTO FechasAbastecimiento (producto_id, proveedor_id, fecha_abastecimiento) VALUES
(4, 1, '2024-07-20'),
(5, 2, '2024-07-25'),
(1, 1, '2024-08-01'),
(2, 2, '2024-08-05'),
(3, 3, '2024-08-10'),
(4, 1, '2024-08-15'),
(5, 2, '2024-08-20'),
(1, 1, '2024-08-25'),
(3, 3, '2024-08-28'),
(5, 2, '2024-08-30');

INSERT INTO TiposPromociones (detalle_promocion) VALUES
("2x1"),
("3x1"),
("3x2"),
("-10%"),
("-20%"),
("-30%"),
("-40%"),
("-50%"),
("-60%");

INSERT INTO Promociones (producto_id, promocion_id) VALUES
(5,3),
(6,4),
(10,5);