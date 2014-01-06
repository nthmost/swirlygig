# Format of LLUV files (tsv):
# 
# Long - Lat - U - V
#
# U: east-west vector
# V: north-south vector

import sys
import pandas as pd
import numpy as np

def parse_time(miltime):
    "take a military-type 24-hr time string (0600), return a postgres-style 24-hr string (06:00:00)"
    try:
        timeint = int(miltime)
    except ValueError:
        return ''

    # assumes a very regular format where sub-10:00 times have an initial 0.
    return '%s:%s:00' % (miltime[:2], miltime[2:4])


def bin_lattice(x):
    inc = 0.001
    return np.sign(x) * np.floor(np.abs(x) / inc) * inc


class LLUV(object):
    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.info = self._parse_filename(filename)
        self.data = self._process()
        self.grid = self._lattice()

    def _parse_filename(self, name):
        """extract important info from filename - is this measured or forecasted?"""
        info = {}

        # name looks like this for measured:
        #       MODL_SFBC_2013_10_02_0600-2013_10_02_0600.txt
        #
        # for forecast, the name times are dissimilar:
        #       MODL_SFBC_2013_10_02_0600-2013_10_02_0630.txt

        parts = name.split('_')

        info['date'] = '%s-%s-%s' % (parts[2], parts[3], parts[4])
        info['time1'] = parse_time(parts[5].split('-')[0])
        info['time2'] = parse_time(parts[8].split('.')[0])

        if info['time1'] == info['time2']:
            info['observed'] = 'TRUE'
        else:
            info['observed'] = 'FALSE'
        return info

    def _process(self):
        """cleans data for Postgres, places into a list of dicts (one dict per coordinate)."""

        f = open(self.filename)
        lines = f.readlines()
        f.close()
        
        data = { 'lat': [], 'lon': [], 'ew': [], 'ns': [] }

        for line in lines:
            if line.strip() is not "":
                try:
                    lon, lat, ew, ns = line.strip().split()
                except ValueError:
                    continue

                # we are cool with NaN as a value in Postgres, but we l
                data['lat'].append(float(lat))
                data['lon'].append(float(lon))
                data['ew'].append(float(ew))
                data['ns'].append(float(ns))
        return data
    
    def _lattice(self):
        df = self.to_dataframe()
        lat_lattice = bin_lattice(df.lat)
        lon_lattice = bin_lattice(df.lon)
        return df.groupby([lat_lattice, lon_lattice])[['ns', 'ew']].mean()
        
    def to_dict(self):
        return self.data

    def to_dataframe(self):
        return pd.DataFrame(self.data)

if __name__=='__main__':
    try:
        filename = sys.argv[1]
    except AttributeError:
        print "Supply a LLUV filename path as argument to this script."
        
    sample = LLUV(filename)
    print sample.grid
    
    
"""
df.lat.map(float).map(bin_lattice)
lat_lattice = df.lat.map(float).map(bin_lattice)
lat_lattice = df.lon.map(float).map(bin_lattice)
lat_lattice = df.lat.map(float).map(bin_lattice)
lon_lattice = df.lon.map(float).map(bin_lattice)
dt
df
df.ns
df.groupby([lat_lattice, lon_lattice])['ns'].mean()
df
df.ns
df.ns.map(float)
df['ns'] = df.ns.map(float)
df.groupby([lat_lattice, lon_lattice])['ns'].mean()
df.groupby([lat_lattice, lon_lattice])['ns'].mean().dropna()
df.groupby([lat_lattice, lon_lattice])['ns'].mean().dropna().reset_index()
df.groupby([lat_lattice, lon_lattice])['ns'].mean().dropna().reset_index().head()
df.groupby([lat_lattice, lon_lattice])[['ns', 'ew']].mean()
df['ew'] = df.ew.map(float)
df.groupby([lat_lattice, lon_lattice])[['ns', 'ew']].mean()
df.groupby([lat_lattice, lon_lattice])[['ns', 'ew']].mean().reset_index()
df.groupby([lat_lattice, lon_lattice])[['ns', 'ew']].mean().reset_index()
df
df
%hist
"""

"""
http://stackoverflow.com/questions/19595643/pandas-is-there-a-natural-way-to-get-the-value-of-a-cell-in-the-previous-row-gi?rq=1
"""