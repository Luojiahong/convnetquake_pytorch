def filter_catalog_time(cat, time_range):
    return cat[(cat.utc_timestamp >= time_range[0])
               & (cat.utc_timestamp <= time_range[1])]


def filter_catalog_space(cat, lon_range, lat_range):
    return cat[
        (cat.longitude >= lon_range[0]) &
        (cat.longitude <= lon_range[1]) &
        (cat.latitude >= lat_range[0]) &
        (cat.latitude <= lat_range[1])
        ]
