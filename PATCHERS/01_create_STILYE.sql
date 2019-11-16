create table adhoc_parser.stilye(
    id serial not null constraint stilye_key primary key,
    articul varchar(255) not null ,
    name_first text null ,
    name_second varchar(500) null ,
    picture text null ,
    main_picture text null ,
    price int null ,
    coating text null ,
    category varchar(500) null ,
    description text null ,
    equipment text null ,
    accessory text null ,
    parse_date date);
CREATE USER stilye WITH password 'stilye';
GRANT all privileges ON  DATABASE parsing_db to stilye;
GRANT ALL ON ALL TABLES IN SCHEMA adhoc_parser to stilye;
GRANT ALL ON ALL SEQUENCES IN SCHEMA adhoc_parser to stilye;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA adhoc_parser to stilye;
GRANT USAGE ON SCHEMA adhoc_parser TO stilye;
commit;