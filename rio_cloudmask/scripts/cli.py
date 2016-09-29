import logging

import click
import numpy as np
import rasterio
from rasterio.rio.options import creation_options
from rasterio.transform import guard_transform

from rio_cloudmask.equations import cloudmask, gdal_nodata_mask

logger = logging.getLogger(__name__)


@click.command('cloudmask')
@click.argument('blue', type=click.Path(exists=True))
@click.argument('green', type=click.Path(exists=True))
@click.argument('red', type=click.Path(exists=True))
@click.argument('nir', type=click.Path(exists=True))
@click.argument('swir1', type=click.Path(exists=True))
@click.argument('swir2', type=click.Path(exists=True))
@click.argument('cirrus', type=click.Path(exists=True))
@click.argument('tirs1', type=click.Path(exists=True))
@click.pass_context
@click.option('--dst-dtype',
              default='uint8',
              type=click.Choice(['uint8', 'uint16']),
              help="Integer data type for output data, default: same as input")
@click.option('--min-filter', default=3, type=int,
              help="removes outliers, clusters of cloud must be > min_filter")
@click.option('--max-filter', default=25, type=int,
              help="grow cloud mask around edges by max_filter pixels")
@click.option('--output', '-o', type=click.Path(exists=False), required=True)
@creation_options
def main(ctx, dst_dtype, output, creation_options,
         blue, green, red, nir, swir1, swir2, cirrus, tirs1,
         min_filter, max_filter):
    """Creates a cloud mask from Landsat 8 TOA input bands

    \b
    INPUT-BANDS:
        Landsat 8 bands, adjusted to TOA reflectance, 0..1
        Required in this order:
            blue (Band 2)
            green (Band 3)
            red (Band 4)
            nir (Band 5)
            swir1 (Band 6)
            swir2 (Band 7)
            cirrus (Band 9)
            tirs1 (Band 10) * brightness temperature C

    \b
    You can use shell expansion to more easily list the arguments:
        rio cloudmask LC8*_B{2,3,4,5,6,7,9}_toa.tif LC8*_B10_temp.tif -o mask.tif

    output is a uint8 single-band tif with 0=cloud/nodata
    """

    # Determine write profile for output
    with rasterio.open(red) as src:
        profile = src.profile.copy()

    profile.update(**creation_options)
    profile['transform'] = guard_transform(profile['affine'])
    dst_dtype = dst_dtype if dst_dtype else profile['dtype']
    profile['dtype'] = dst_dtype

    # process filter opts
    if min_filter == 0:
        min_filter = None
    else:
        # 2d shape implied
        min_filter = (min_filter, min_filter)

    if max_filter == 0:
        max_filter = None
    else:
        # 2d shape implied
        max_filter = (max_filter, max_filter)

    # Read all bands into memory
    # Due to the global (scene-wide) nature of the algorithm,
    # an independent window approach isn't easy
    # TODO make this more parallelizable and memory efficient
    logger.info("Reading input bands")
    arrs = [rasterio.open(path).read(1)
            for path in (blue, green, red, nir, swir1, swir2, cirrus, tirs1)]

    # Thermal band defines basic nodata mask
    tirs_arr = arrs[-1]

    # Quiet warnings related to NaNs and infs
    np.seterr(invalid='ignore', divide='ignore')

    # Potential Cloud Layer
    logger.info("Calculating mask")
    pcl, pcsl = cloudmask(*arrs, min_filter=min_filter, max_filter=max_filter)
    gmask = gdal_nodata_mask(pcl, pcsl, tirs_arr)

    logger.info("Writing mask")
    with rasterio.open(output, 'w', **profile) as dst:
        dst.write(gmask, 1)
