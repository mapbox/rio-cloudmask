#!/usr/bin/env python

import click
import rasterio

from rio_cloudmask.equations import cloudmask


@click.command()
def main():
    pref = 'testdata/LC80130312015295LGN00_'
    blue = rasterio.open(pref + "B2_toa.tif").read(1)
    green = rasterio.open(pref + "B3_toa.tif").read(1)
    red = rasterio.open(pref + "B4_toa.tif").read(1)
    nir = rasterio.open(pref + "B5_toa.tif").read(1)
    swir1 = rasterio.open(pref + "B6_toa.tif").read(1)
    swir2 = rasterio.open(pref + "B7_toa.tif").read(1)
    cirrus = rasterio.open(pref + "B9_toa.tif").read(1)
    tirs1 = rasterio.open(pref + "B10_toa.tif").read(1)

    with rasterio.open(pref + "B2_toa.tif") as src1:
        profile = src1.profile

    profile['dtype'] = 'uint8'

    clouds, shadows = cloudmask(
        blue, green, red, nir, swir1, swir2, cirrus, tirs1)

    with rasterio.open('pcl.tif', 'w', **profile) as dst:
        dst.write((~(clouds | shadows) * 255).astype('uint8'), 1)


if __name__ == "__main__":
    main()
