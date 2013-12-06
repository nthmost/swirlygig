import os
import sys

outfilename = 'import/2013-10.dump'

dbname = 'baycurrents';
tablename = 'currents';

fout = open(outfilename, 'w')

sql_insert_tmpl = "INSERT INTO "+tablename+" VALUES ('{date}', '{time1}', '{time2}', {observed}, {lat}, {lon}, {ew}, {ns});\n"

def write_sql(datadict):
    """expects datadict with:
    date        (string)
    time1       (string)
    time2       (string)
    observed    (bool)
    lat (float)
    lon (float)
    ew  (float)
    ns  (float)
    """
    fout.write(sql_insert_tmpl.format(**datadict))
    fout.flush()

def parse_time(miltime):
    "take a military-type 24-hr time string (0600), return a postgres-style 24-hr string (06:00:00)"
    try:
        timeint = int(miltime)
    except ValueError:
        return ''

    # assumes a very regular format where sub-10:00 times have an initial 0.
    return '%s:%s:00' % (miltime[:2], miltime[2:4])


def parse_filename(name):
    """extract important info from filename - is this measured or forecasted?"""
    data = {}

    # name looks like this for measured:
    #       MODL_SFBC_2013_10_02_0600-2013_10_02_0600.txt
    #
    # for forecast, the name times are dissimilar:
    #       MODL_SFBC_2013_10_02_0600-2013_10_02_0630.txt

    parts = name.split('_')

    data['date'] = '%s-%s-%s' % (parts[2], parts[3], parts[4])
    data['time1'] = parse_time(parts[5].split('-')[0])
    data['time2'] = parse_time(parts[8].split('.')[0])

    if data['time1'] == data['time2']:
        data['observed'] = 'TRUE'
    else:
        data['observed'] = 'FALSE'
    return data
 

def process(lines, filename):
    """cleans data for Postgres, places into a list of dicts (one dict per coordinate)."""

    filename_dict = parse_filename(filename))

    for line in lines:
        if line.strip() is not "":
            try:
                lon, lat, ew, ns = line.strip().split()
            except ValueError:
                continue

            # we are cool with NaN as a value in Postgres.
            data = { 'lat': lat, 'lon': lon, 'ew': ew, 'ns': ns }

            data.update(filename_dict)  
            write_sql(data)
    print "finished %s" % filename 


def main(targetdir):
    for lluv in os.listdir(targetdir):
        fh = open(os.path.join(targetdir, lluv))
        process(fh.readlines(), lluv)
        fh.close()
    print "done"


if __name__=='__main__':

    try:
        datadir = sys.argv[1]
    except:
        print "supply directory as argument to this script"
        sys.exit()

    main(datadir)


# calculating direction and magnitude of composite vectors in Postgres:
#    select degrees(atan2(3.7823820e+01, -1.2247408e+02)) as direction, |/(-19.43^2 + -3.879^2) as magnitude;
