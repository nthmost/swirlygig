
#U: east-west vector
#V: north-south vector

#Long - Lat - U - V



def parse_time(miltime):
    "take a military-type 24-hr time string (0600), return a postgres-style 24-hr string (06:00:00)"
    try:
        timeint = int(miltime)
    except ValueError:
        return ''

    # assumes a very regular format where sub-10:00 times have an initial 0.
    return '%s:%s:00' % (miltime[:2], miltime[2:4])


class LLUVsnapshot(object):
    def __init__(self, filename, **kwargs):
        self.filename = filename

    def _parse_filename(self, name):
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

        

    def to_dict(self):
        return self.datadict

    def to_dataframe(self):
        return pandas.DataFrame(self.datadict)

