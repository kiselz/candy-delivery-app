DROP TABLE IF EXISTS courier_type;
DROP TABLE IF EXISTS courier;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS working_hours;

CREATE TABLE courier_type (
    id INTEGER PRIMARY KEY,
    type VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO courier_type (id, type)
VALUES
    (1, 'foot'),
    (2, 'bike'),
    (3, 'car');


CREATE TABLE regions (
    courier_id INTEGER,
    region INTEGER NOT NULL,
    CONSTRAINT fk_courier FOREIGN KEY (courier_id) REFERENCES courier (id)
);

CREATE TABLE working_hours (
    courier_id INTEGER,
    work_start TIME NOT NULL,
    work_end TIME NOT NULL
);

CREATE TABLE courier (
    id INTEGER PRIMARY KEY,
    courier_type_id INTEGER NOT NULL,
    rating FLOAT(2, 1) DEFAULT 0.0 NOT NULL,
    earnings INTEGER DEFAULT 0 NOT NULL,
  	CONSTRAINT fk_courier_type FOREIGN kEY (courier_type_id) REFERENCES courier_type (id),
    CONSTRAINT fk_regions FOREIGN KEY (id) REFERENCES regions (courier_id),
    CONSTRAINT fk_working_hours FOREIGN KEY (id) REFERENCES working_hours (courier_id)
);
