create table adhoc_parser.qq_stilye(
    id serial not null constraint qq_stilye_key primary key,
    articul varchar(255) not null ,
    enable varchar(500) null ,
    code varchar(255) not null ,
    price int null ,
    name varchar(500) not null ,
    link varchar(500) not null ,
    main_pic text null ,
    other_pic text null ,
    path varchar(255) not null ,
    feature text null ,
    description text null ,
    parse_date date);
--CREATE USER qq_stilye WITH password 'qq_stilye';
--GRANT all privileges ON  DATABASE parsing_db to qq_stilye;
GRANT ALL ON ALL TABLES IN SCHEMA adhoc_parser to qq_stilye;
GRANT ALL ON ALL SEQUENCES IN SCHEMA adhoc_parser to qq_stilye;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA adhoc_parser to qq_stilye;
GRANT USAGE ON SCHEMA adhoc_parser TO qq_stilye;
commit;
