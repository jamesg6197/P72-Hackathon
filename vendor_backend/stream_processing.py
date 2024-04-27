import csp
import httpx
import os
import pandas as pd
import folium


from folium.plugins import HeatMap
from csp import ts
import numpy as np

from datetime import datetime, timedelta
from .urls import CITIBIKE_STATION_INFORMATION, CITIBIKE_STATION_STATUS
from .models import ActivityHeatmapData, RegionalDataHeatmap

from .latlon import NYC_LOCATIONS



def get_stations():
    dat = httpx.get(CITIBIKE_STATION_INFORMATION).json()
    to_return = {station["station_id"]: station for station in dat["data"]["stations"]}
    # Let's remove the rental uris
    for station in to_return.values():
        station.pop("rental_uris", None)
    return to_return

def get_station_status():
    print("hello")

    dat = httpx.get(CITIBIKE_STATION_STATUS).json()["data"]["stations"]
    stations = get_stations()
    
    for record in dat:
        record.pop("vehicle_types_available", None)
        record.update(stations[record["station_id"]])
    ret = pd.json_normalize(dat)
    ret["last_reported"] = pd.to_datetime(ret["last_reported"], unit = 's')
    return ret

@csp.node
def poll_data(interval: timedelta) -> ts[pd.DataFrame]:

    with csp.alarms():
        a_poll = csp.alarm(bool)

    with csp.start():
        csp.schedule_alarm(a_poll, timedelta(), True)

    if csp.ticked(a_poll):
    
        to_return = get_station_status()

        # schedule next poll in `interval`
        csp.schedule_alarm(a_poll, interval, True)
        return to_return

def find_closest_region(lat, lon, regions_dict):
    return min(regions_dict.keys(), key=lambda x: np.sqrt((regions_dict[x][0] - lat)**2 + (regions_dict[x][1] - lon)**2)) 
@csp.node
def diff_(x: ts[pd.DataFrame], x_delay: ts[pd.DataFrame]) -> ts[pd.DataFrame]:
    if csp.ticked(x) and csp.valid(x, x_delay):
        current_capacity_data = x[["station_id", "num_bikes_available", "last_reported", "capacity", "lat", "lon"]].sort_values("station_id")
        past = x_delay[["station_id",  "num_bikes_available", "last_reported", "capacity", "lat", "lon"]].sort_values("station_id")
        data_with_diffs = current_capacity_data.copy()
        
        data_with_diffs["rounded_lon"] = data_with_diffs["lon"].round(1)
        data_with_diffs["rounded_lat"] = data_with_diffs["lat"].round(1)

       

        data_with_diffs['region'] = current_capacity_data.apply(lambda row: find_closest_region(row['lat'], row['lon'], NYC_LOCATIONS), axis=1)



        data_with_diffs = data_with_diffs.groupby(['rounded_lat', 'rounded_lon']).apply(
            lambda x: x.nlargest(50, 'capacity')
        ).reset_index(drop=True)

        data_with_diffs["changing"] = current_capacity_data["last_reported"] - past["last_reported"]
        data_with_diffs["num_bike_diff"] = abs(current_capacity_data["num_bikes_available"] - past["num_bikes_available"])
        
        print(data_with_diffs["changing"].value_counts())
        print(data_with_diffs["num_bike_diff"].value_counts())
        return data_with_diffs
    
@csp.node
def make_heat_map(x: ts[pd.DataFrame]):
    map_center = [x['lat'].mean(), x['lon'].mean()]
    map = folium.Map(location=map_center, zoom_start=9)
    heat_data = []
    current_time = datetime.utcnow()

    regional_data = x.groupby(["region"]).agg(
        {
            "num_bike_diff": "sum"
        }
    ).reset_index()
    regional_data = regional_data.rename(columns = {"num_bike_diff": "total_activity"})
    for _, row in regional_data.iterrows():
        print(row)
        RegionalDataHeatmap.objects.create(
            region = row["region"],
            total_activity = row["total_activity"],
            #total_profitability = 0,
        )

    for _, row in x.iterrows():
        # Append to heatmap data list for folium
        heat_data.append([row['lat'], row['lon'], row['num_bike_diff']])
        ActivityHeatmapData.objects.create(
            latitude=row['lat'],
            longitude=row['lon'],
            intensity=row['num_bike_diff'],
            timestamp = current_time
        )
        
        # Create a new HeatmapData object and save to the database

    # Add heatmap layer to the map
    # HeatMap(heat_data).add_to(map)
    # map.save(f'{os.getcwd()}/vendor_backend/html_forms/heatmap.html')

        
@csp.graph
def main_graph(interval: timedelta = timedelta(seconds=60)) -> ts[pd.DataFrame]:
    data = poll_data(interval)
    data_lagged = csp.delay(data, 1)
    res = diff_(data, data_lagged)
    make_heat_map(res)
    csp.print("res", res)
    return res

# def main():
#     csp.run(main_graph, realtime = True, starttime = datetime.utcnow())
    
# if __name__ == "__main__":
#     main()

