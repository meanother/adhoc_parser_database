drop table adhoc_parser.sunerzsha;
create table adhoc_parser.sunerzsha (
    id serial not null constraint sunerzsha_key primary key,
    item_id varchar(255) not null,
    name varchar(255) not null,
    category_first varchar(255) null,
    category_second varchar(255) null,
    price int not null,
    accessibility varchar(255) null,
    link varchar(255) null,
    pics text null,
    files text null,
    featurecs text null,
    additional_componentscs text null,
    extra_option text null,
    accessoriescs text null,
    parse_date date
    );
GRANT ALL ON ALL TABLES IN SCHEMA adhoc_parser to sunerzha;
GRANT ALL ON ALL SEQUENCES IN SCHEMA adhoc_parser to sunerzha;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA adhoc_parser to sunerzha;
GRANT USAGE ON SCHEMA adhoc_parser TO sunerzha;
commit;