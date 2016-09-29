# pylint: disable=W0621
from click.testing import CliRunner
import numpy as np
import pytest
import rasterio

from rio_cloudmask.scripts.cli import main


@pytest.fixture
def inputs():
    pref = 'tests/data/LC80130312015295LGN00_'
    data = [
        pref + "B2_toa.tif",
        pref + "B3_toa.tif",
        pref + "B4_toa.tif",
        pref + "B5_toa.tif",
        pref + "B6_toa.tif",
        pref + "B7_toa.tif",
        pref + "B9_toa.tif",
        pref + "B10_toa.tif"]
    return data


def test_output(tmpdir, inputs):
    output = str(tmpdir.join('test.tif'))
    runner = CliRunner()

    result = runner.invoke(
        main, inputs + ['-o', output])

    assert result.exit_code == 0
    with rasterio.open(output) as src:
        assert src.count == 1
        assert src.meta['dtype'] == 'uint8'
        arr = src.read(1)
        assert sorted(list(np.unique(arr))) == [0, 255]  # only 0 and 255 values


def test_nofilter(tmpdir, inputs):
    output = str(tmpdir.join('test.tif'))
    runner = CliRunner()

    result = runner.invoke(
        main, inputs + ['--min-filter', '0',
                        '--max-filter', '0',
                        '-o', output])

    assert result.exit_code == 0
    with rasterio.open(output) as src:
        assert src.count == 1
        assert src.meta['dtype'] == 'uint8'
        arr = src.read(1)
        assert sorted(list(np.unique(arr))) == [0, 255]  # only 0 and 255 values
