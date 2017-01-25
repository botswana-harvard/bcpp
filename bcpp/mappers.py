from edc_map.site_mappers import site_mappers

from edc_map.mapper import Mapper

from .landmarks import TEST_LANDMARKS


class AnonymousMapper(Mapper):

    map_area = 'austin'
    map_code = '88'
    center_lat = -30.2671500
    center_lon = 97.7430600
    radius = 100.5
    location_boundary = ()

    intervention = True
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS
    landmarks = None

site_mappers.register(AnonymousMapper)


class TestPlotMapper(Mapper):

    map_area = 'test_community'
    map_code = '01'
    pair = 0
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS

    landmarks = TEST_LANDMARKS

    center_lat = -25.330451
    center_lon = 25.556502
    radius = 100.5
    location_boundary = ()

    intervention = True

site_mappers.register(TestPlotMapper)


class BokaaPlotMapper(Mapper):

    map_area = 'bokaa'
    map_code = '17'
    pair = 0
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS

    landmarks = TEST_LANDMARKS

    center_lat = -24.425856
    center_lon = 26.021626
    radius = 100.5
    location_boundary = ()

    intervention = False

site_mappers.register(BokaaPlotMapper)


class DigawanaPlotMapper(Mapper):

    map_area = 'digawana'
    map_code = '12'
    pair = 0
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS

    landmarks = TEST_LANDMARKS

    center_lat = -25.330451
    center_lon = 25.556502
    radius = 100.5
    location_boundary = ()

    intervention = True

site_mappers.register(DigawanaPlotMapper)


class GumarePlotMapper(Mapper):

    map_area = 'gumare'
    map_code = '35'
    pair = 13
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS

    landmarks = TEST_LANDMARKS

    center_lat = -19.359734
    center_lon = 22.163286
    radius = 100.5
    location_boundary = ()

    intervention = True

site_mappers.register(GumarePlotMapper)


class GwetaPlotMapper(Mapper):

    map_area = 'gweta'
    map_code = '34'
    pair = 13
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS

    landmarks = TEST_LANDMARKS

    center_lat = -20.205621
    center_lon = 25.251474
    radius = 100.5
    location_boundary = ()

    intervention = True

site_mappers.register(GwetaPlotMapper)
