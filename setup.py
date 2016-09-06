import os
from setuptools import setup, find_packages

with open('rio_cloudmask/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break

long_description = """
Rasterio plugin for identifying clouds in multi-spectral satellite imagery.

See https://github.com/mapbox/rio-cloudmask for docs."""

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


inst_reqs = ["click", "rasterio", "rio-mucho", 'scipy']

setup(
    name='rio-cloudmask',
    version=version,
    description=u"Cloud masking plugin for rasterio",
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: GIS'],
    keywords='',
    author=u"Matthew Perry",
    author_email='perrygeo@gmail.com',
    url='https://github.com/mapbox/rio-cloudmask',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require={
        'test': ['pytest', 'pytest-cov', 'codecov'],
    },
    entry_points="""
    [rasterio.rio_plugins]
    cloudmask=rio_cloudmask.scripts.cli:main
    """)
