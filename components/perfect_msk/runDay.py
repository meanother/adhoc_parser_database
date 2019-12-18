import subprocess


def get_componentns():

    command = '''
    psql -U semenov -d parsing_db -h localhost -w -c "select * from ([B
    select name 'oracdecor_KAFKA',count(*), parse_date from adhoc_parser.oracdecor where parse_date = '18.12.2019' group by parse_date
    union
    select name 'kludi_com',count(*), parse_date from adhoc_parser.kludi_com where parse_date = '18.12.2019' group by parse_date
    union
    select name 'grohe', count(*), parse_date from adhoc_parser.grohe where parse_date = '18.12.2019' group by parse_date
    union
    select name 'pergo', count(*), parse_date from adhoc_parser.pergo where parse_date = '18.12.2019' group by parse_date
    union
    select name 'pratta', count(*), parse_date from adhoc_parser.pratta where parse_date = '18.12.2019' group by parse_date
    union
    select name 'quick-step', count(*), parse_date from adhoc_parser.quick_step where parse_date = '18.12.2019' group by parse_date
    union
    select name 'sunerzha', count(*), parse_date from adhoc_parser.sunerzha where parse_date = '18.12.2019' group by parse_date
    union
    select name 'stilye', count(*), parse_date from adhoc_parser.stilye where parse_date = '18.12.2019' group by parse_date
    union
    select name 'qq_stilye', count(*), parse_date from adhoc_parser.qq_stilye where parse_date = '18.12.2019' group by parse_date
    union
    select name 'perfect_msk', count(*), parse_date from adhoc_parser.perfect_msk where parse_date = '18.12.2019' group by parse_date
    ) as foo
    order by name;"
    '''


    comps = []
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    command.stdin.write(b'12345')
    command.stdin.close()
    command.stdout.read()

    print(command)
    components = command.communicate()
    print(components)
    for i in components:
        try:
            component = i.decode('utf-8')
            comps.append(component)
        except AttributeError:
            pass
    return comps

get_componentns()