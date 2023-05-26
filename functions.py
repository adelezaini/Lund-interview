###### This python file collects fuctions to support the notebooks
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def climatology_mean(ds, time_res="month"):  # test for season too
    """Evaluate the 'time_res'-ly (i.e. monthly) mean, weighted on the days"""
    # Make a DataArray with the number of days in each month, size = len(time)
    attrs = ds.attrs
    month_length = ds.time.dt.days_in_month

    # Calculate the weights by grouping by 'time.season'
    weights = month_length.groupby("time."+time_res) / month_length.groupby("time."+time_res).sum()

    # Test that the sum of the weights for each season is 1.0
    np.testing.assert_allclose(weights.groupby("time."+time_res).sum().values, np.ones(len(month_length.groupby("time."+time_res).sum().values)))

    # Calculate the weighted average
    wm = (ds * weights).groupby("time."+time_res).sum(dim="time")
    wm.attrs = attrs
    return wm

def annual_climatology(ds):
    """Evaluate the annual climatological mean, through evaluating the annual cycle first.
    Return an array"""
    attrs = ds.attrs
    ds_clim = climatology_mean(ds, "month")
    m = ds_clim.mean(dim = "month")
    m.attrs = attrs
    return m

def match_coord(original_coord_da, coord_to_match_da, method='linear'):
    """Return DataArray with matching coordinates (lon/lat) with another given DataArray.
    The method used is the interp() of xarray. Different options of interpolation are available.
    Args:
    - original_coord_da (DataArray): variable with coordinates to be matched
    - coord_to_match_da (DataArray): variable with coordinates to match
    - method ({"linear", "nearest", "zero", "slinear", "quadratic", "cubic", "polynomial"},
    default: "linear"): the method used to interpolate.
    """
    new_da = original_coord_da.copy()
    new_da = new_da.interp(lat=coord_to_match_da['rlat'], method = method)
    new_da = new_da.interp(lon=coord_to_match_da['rlon'], method = method)
    return new_da
    
def ax_map_properties(ax, alpha=0.3, coastlines=True, gridlines=True, earth = False, ocean=True, land=True, borders=True, rivers=True, provinces=False):
    """Set default map properties on the axis"""
    if coastlines: ax.coastlines()
    if ocean: ax.add_feature(cartopy.feature.OCEAN, zorder=10, edgecolor='k')#, alpha=alpha)
    if land: ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black', alpha=alpha)
    if borders: ax.add_feature(cfeature.BORDERS, alpha=0.3)
    if rivers: ax.add_feature(cfeature.RIVERS)
    if earth: ax.stock_img()
    if gridlines: ax.gridlines(alpha=0.2, zorder=100, color='black')

