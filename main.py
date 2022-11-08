import xarray as xr
import numpy as np
from holoviews import opts
import datetime
import holoviews as hv
import matplotlib.pyplot as plt

dat= xr.open_zarr("s3://veda-data-store-staging/EIS/zarr/FWI.GEOS-5.zarr")

def generate_plot(lon,lat):
    arr=dat.sel(lon=lon,lat=lat)['GEOS-5_FWI']
    df=arr.to_dataframe(name=None, dim_order=None).drop(columns=["lat","lon"]).reset_index()
    tmp = np.array([np.roll(np.array(df.query(f"forecast=={i}")["GEOS-5_FWI"]), i) for i in range(9)])
    for i in range(len(tmp)):
        tmp[i,:i]=np.NaN

    plt.figure(figsize=(20,5))
    plt.pcolormesh(df.time.unique(), [f"lag_{i}" for i in df.forecast.unique()],tmp, cmap="rainbow")
    plt.colorbar(label="FWI")
    plt.title("FWI Index Plot ")
    plt.ylabel("Lead time in days")
    plt.xlabel("Date")
    plt.show()

generate_plot(130.9375,-0.25)
