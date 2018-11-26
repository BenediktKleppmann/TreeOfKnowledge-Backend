DROP TABLE IF EXISTS ObjectTypes;
DROP TABLE IF EXISTS ObjectAttributes;
DROP TABLE IF EXISTS ObjectIdentifiers; 
DROP TABLE IF EXISTS Objects;
DROP TABLE IF EXISTS Uploads; 
DROP TABLE IF EXISTS DataPoints;
DROP TABLE IF EXISTS HierachicalTrees;

DROP TABLE IF EXISTS object_types;
DROP TABLE IF EXISTS object_attributes;
DROP TABLE IF EXISTS object_identifiers; 
DROP TABLE IF EXISTS objects;
DROP TABLE IF EXISTS uploads; 
DROP TABLE IF EXISTS data_points;
DROP TABLE IF EXISTS hierachical_trees;  


CREATE TABLE object_types(
    object_type text not null,
    possible_attributes text[],
    PRIMARY KEY(object_type)
);


INSERT INTO object_types (object_type) VALUES ('Person');
INSERT INTO object_types (object_type) VALUES ('Animal');


CREATE TABLE object_attributes (
    most_general_object_type text not null REFERENCES object_types(object_type),
    attribute_name text not null,
    data_type text NOT NULL,
    tdda_value_requirement json not null,
    regex_value_requirement text,
    PRIMARY KEY(attribute_name)
);


INSERT INTO object_attributes (most_general_object_type, attribute_name, data_type, tdda_value_requirement, regex_value_requirement) 
		      VALUES ('Person',                 'First Name',   'String',  '{"type":"string", "min_length":3, "max_length":11}', '["^[A-Z][a-z]+$", "^[A-Z]\\. [A-Z][a-z]+$"]');

INSERT INTO object_attributes (most_general_object_type, attribute_name, data_type, tdda_value_requirement, regex_value_requirement) 
		      VALUES ('Person',                 'Last Name',   'String',  '{"type":"string", "min_length":4, "max_length":15}', '["^[A-Za-z]+$", "^[A-Z][a-z]+ [A-Z][a-z]+$"]' );

INSERT INTO object_attributes (most_general_object_type, attribute_name, data_type, tdda_value_requirement) 
		      VALUES ('Animal',                 'Date of Birth',   'String',  '{"type": "date", "min":"1954-04-26 00:00:00", "max":"2009-12-17 00:00:00"}' );

INSERT INTO object_attributes (most_general_object_type, attribute_name, data_type, tdda_value_requirement, regex_value_requirement) 
		      VALUES ('Animal',                 'Place of Birth','String',  '{"type":"string", "min_length":4, "max_length":25}', '["^[A-Za-z]+$", "^[A-Z][a-z]+ [A-Z][a-z]+$"]' );

INSERT INTO object_attributes (most_general_object_type, attribute_name, data_type, tdda_value_requirement) 
		      VALUES ('Animal',                 'Activity', 'String',  '{"type":"string", "min_length":7, "max_length":8, "max_nulls":0, "allowed_values":["sleeping", "working"]}');





CREATE TABLE object_identifiers (
    object_type text not null REFERENCES object_types(object_type),
    unique_column_combination text[],
    PRIMARY KEY(object_type, unique_column_combination)
);


INSERT INTO object_identifiers (object_type, unique_column_combination) VALUES ('Person', '{"First Name", "Last Name", "Date of Birth", "Place of Birth"}');



CREATE TABLE objects (
    object_id serial primary key,
    object_type text not null REFERENCES object_types(object_type),
    identifying_attributes json not null,
    object_name text not null
);

INSERT INTO objects (object_type, identifying_attributes, object_name)
  	     VALUES ('Person', '{"First Name":"Benedikt", "Last Name":"Kleppmann", "Date of Birth":"1989-06-14", "Place of Birth":"Munich"}', 'Benedikt_Kleppmann');




CREATE TABLE uploads (
    upload_id serial primary key,
    userid int NOT NULL,
    table_source text NOT NULL,
    table_name text NOT NULL,
    upload_timestamp int NOT NULL,
    upload_specifications json NOT NULL
);


INSERT INTO uploads (userid, table_source, table_name, upload_timestamp, upload_specifications)
             VALUES (9, 'direct observation from user', '',  1543158660, '{}');



CREATE TABLE data_points (
    object_type text NOT NULL REFERENCES object_types(object_type),
    object_id int NOT NULL REFERENCES objects(object_id),
    attribute_name text NOT NULL REFERENCES object_attributes(attribute_name),
    attribute_value text NOT NULL,
    valid_time int[2] NOT NULL,
    uncertainty text,
    upload_id int,
    table_source text 
);


INSERT INTO data_points (object_type, object_id, attribute_name, attribute_value, valid_time, upload_id, table_source)
                VALUES ('Person', 1, 'Activity', 'working', '{1543158660, 1543158760}', 1, 'direct observation from user');



/*

CREATE TABLE hierachical_trees (
    tree_name text NOT NULL,
    networkx_graph json NOT NULL,
    tree_elements text[],
    PRIMARY_KEY(tree_name)
);

INSERT INTO hierachical_trees VALUES ('ObjectHierachy', '{"object":["physical_object", "group_of_objects", "etc"]}', '{"object", "physical_object", "group_of_objects", "etc"}')
INSERT INTO hierachical_trees VALUES ('Environment', '{"universe":["on_or_in_earth", "in_space", "around_celestrial object"]}', '{"universe", "on_or_in_earth", "in_space", "around_celestrial object"}')

*/



