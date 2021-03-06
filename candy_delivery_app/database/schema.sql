DROP TABLE IF EXISTS courier_type;
DROP TABLE IF EXISTS courier;
DROP TABLE IF EXISTS couriers_regions;
DROP TABLE IF EXISTS couriers_working_hours;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orders_delivery_hours;
DROP TABLE IF EXISTS couriers_with_orders;
DROP TABLE IF EXISTS couriers_assigned_time;

CREATE TABLE courier_type (
    id INTEGER PRIMARY KEY,
    type VARCHAR(20) NOT NULL UNIQUE,
    weight INTEGER NOT NULL
);

INSERT INTO courier_type (id, type, weight)
VALUES
    (1, 'foot', 10),
    (2, 'bike', 15),
    (3, 'car', 50);


CREATE TABLE couriers_regions (
    courier_id INTEGER,
    region INTEGER NOT NULL,
    CONSTRAINT fk_courier FOREIGN KEY (courier_id) REFERENCES courier (id)
);

CREATE TABLE couriers_working_hours (
    courier_id INTEGER,
    work_start VARCHAR(5) NOT NULL,
    work_end VARCHAR(5) NOT NULL
);

CREATE TABLE courier (
    courier_id INTEGER PRIMARY KEY,
    courier_type VARCHAR(20) NOT NULL,
    rating FLOAT(2, 1) DEFAULT 0.0 NOT NULL,
    earnings INTEGER DEFAULT 0 NOT NULL,
    CONSTRAINT fk_courier_type FOREIGN KEY (courier_type) REFERENCES courier_type (type),
    CONSTRAINT fk_couriers_regions FOREIGN KEY (courier_id) REFERENCES couriers_regions (courier_id),
    CONSTRAINT fk_working_hours FOREIGN KEY (courier_id) REFERENCES couriers_working_hours (courier_id)
);

CREATE TABLE orders_delivery_hours (
    order_id INTEGER,
    delivery_start TIME NOT NULL,
    delivery_end TIME NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    weight FLOAT NOT NULL,
    region INTEGER NOT NULL,
    is_assigned BOOL DEFAULT 0 NOT NULL,
    CONSTRAINT fk_delivery_hours FOREIGN KEY (order_id) REFERENCES orders_delivery_hours (order_id)
);

CREATE TABLE couriers_with_orders (
    courier_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    assigned_time VARCHAR(255) NOT NULL,
    is_completed BOOL DEFAULT 0 NOT NULL,
    completed_time VARCHAR(255)
);

CREATE TABLE couriers_assigned_time (
    courier_id INTEGER PRIMARY KEY,
    assigned_time VARCHAR(255) NOT NULL
);