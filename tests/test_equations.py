# pylint: disable=W0621
import numpy as np
import pytest
import rasterio

from rio_cloudmask.equations import cloudmask


@pytest.fixture
def bands():
    pref = 'tests/data/LC80130312015295LGN00_'
    data = dict(
        blue=rasterio.open(pref + "B2_toa.tif").read(1),
        green=rasterio.open(pref + "B3_toa.tif").read(1),
        red=rasterio.open(pref + "B4_toa.tif").read(1),
        nir=rasterio.open(pref + "B5_toa.tif").read(1),
        swir1=rasterio.open(pref + "B6_toa.tif").read(1),
        swir2=rasterio.open(pref + "B7_toa.tif").read(1),
        cirrus=rasterio.open(pref + "B9_toa.tif").read(1),
        tirs1=rasterio.open(pref + "B10_toa.tif").read(1))
    return data


def test_cloudmask(bands):
    pcl, pcsl = cloudmask(**bands)
    assert pcl.dtype == np.dtype('bool')
    assert pcsl.dtype == np.dtype('bool')
