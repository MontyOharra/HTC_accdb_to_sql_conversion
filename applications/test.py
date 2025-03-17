from src.utils.normalizeConversionDefinitions.helpers import printCountries, countryGet, printSubdivisions

from isocodes import subdivisions_countries, countries


if __name__ == '__main__':
    print(countryGet(name='united states'))