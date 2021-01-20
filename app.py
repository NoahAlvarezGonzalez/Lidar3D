import googlemaps
import pyproj
import rasterio
from raster2xyz.raster2xyz import Raster2xyz
from rasterio.mask import mask
from vtkplotter import *
import pandas as pd
from scipy.spatial import Delaunay


def adress_to_location(address):
    gmaps_key = googlemaps.Client(key="AIzaSyD5aTjEmCYVsehYPCCVNk_O3-p3xRp65mY")
    address = address
    geocode_result = gmaps_key.geocode(address)
    geocode_result

    postcode = int(geocode_result[0]['address_components'][-1]['long_name'])
    lat = float((geocode_result[0]["geometry"]["location"]["lat"]))
    lng = float((geocode_result[0]["geometry"]["location"]["lng"]))

    print("Latitude = " + str(lat) + " / Longitude = " + str(lng) + " / Postcode = " + str(postcode))

    coord = {"Latitude": lat, "Longitude": lng, "Postcode": postcode}

    return coord



def proj(coord):

    inProj = pyproj.Proj(init='epsg:4326')
    outProj = pyproj.Proj(init='epsg:31370')

    x1, y1 = (coord["Longitude"], coord["Latitude"])

    x2, y2 = pyproj.transform(inProj, outProj, x1, y1)

    print(x2, y2)

    return x2, y2


def setting_path():
    dtm_hainaut = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DTM 2013-2014/DTM_HAINAUT/RELIEF_WALLONIE_MNT_2013_2014.tif'
    dsm_hainaut = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DSM 2013-2014/DSM_HAINAUT/RELIEF_WALLONIE_MNS_2013_2014.tif'

    dtm_liege = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DTM 2013-2014/RELIEF_WALLONIE_MNT_2013_2014_GEOTIFF_31370_PROV_LIEGE/RELIEF_WALLONIE_MNT_2013_2014.tif'
    dsm_liege = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DSM 2013-2014/DSM_LIEGE/RELIEF_WALLONIE_MNS_2013_2014.tif'

    dtm_namur = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DTM 2013-2014/RELIEF_WALLONIE_MNT_2013_2014_GEOTIFF_31370_PROV_NAMUR/RELIEF_WALLONIE_MNT_2013_2014.tif'
    dsm_namur = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DSM 2013-2014/DSM_NAMUR/RELIEF_WALLONIE_MNS_2013_2014.tif'

    dtm_luxembourg = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DTM 2013-2014/RELIEF_WALLONIE_MNT_2013_2014_GEOTIFF_31370_PROV_LUXEMBOURG/RELIEF_WALLONIE_MNT_2013_2014.tif'
    dsm_luxembourg = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DSM 2013-2014/DSM_LUXEMBOURG/RELIEF_WALLONIE_MNS_2013_2014.tif'

    dtm_brabant = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DTM 2013-2014/DTM_BRABANT_WALLON/RELIEF_WALLONIE_MNT_2013_2014.tif'
    dsm_brabant = '/Users/noahalvarezgonzalez/Dataset Wallonie/Wallonia/DSM 2013-2014/DSM_BRABANT_WALLON/RELIEF_WALLONIE_MNS_2013_2014.tif'

    path = {"Hainaut_DTM": dtm_hainaut, "Hainaut_DSM": dsm_hainaut,
            "Liege_DTM": dtm_liege, "Liege_DSM": dsm_liege,
            "Namur_DTM": dtm_namur, "Namur_DSM": dsm_namur,
            "Luxembourg_DTM": dtm_luxembourg, "Luxembourg_DSM": dsm_luxembourg,
            "Brabant_DTM": dtm_brabant, "Brabant_DSM": dsm_brabant}

    return path


def selecting_path(path, coord):

    postcode = coord["Postcode"]

    if 1300 <= postcode < 1500:
        path_dsm = path["Brabant_DSM"]
        path_dtm = path["Brabant_DTM"]
        print('Brabant Wallon')

    elif 4000 <= postcode < 5000:
        path_dsm = path["Liege_DSM"]
        path_dtm = path["Liege_DTM"]
        print('Liège')

    elif 5000 <= postcode < 6000:
        path_dsm = path["Namur_DSM"]
        path_dtm = path["Namur_DTM"]
        print('Namur')

    elif (6000 <= postcode < 6600) or (7000 <= postcode < 8000):
        path_dsm = path["Hainaut_DSM"]
        path_dtm = path["Hainaut_DTM"]
        print('Hainaut')

    else:
        path_dsm = path["Luxembourg_DSM"]
        path_dtm = path["Luxembourg_DTM"]
        print("Luxembourg")

    choosen_path = {"Path_DSM": path_dsm, "Path_DTM": path_dtm}
    print(choosen_path.values())
    return choosen_path

def square(x,y,r):
    geojson = [{'type': 'Polygon', 'coordinates': [[(x - r, y - r),
                                                    (x + r, y - r),
                                                    (x + r, y + r),
                                                    (x - r, y + r)]]}]
    return geojson


def rasteriser(x2, y2, choosen_path, path_name, file_name):

    geoms = square(x2, y2, 200)

    # Load the raster, mask it by the polygon and crop it
    with rasterio.open(choosen_path[path_name]) as src:
        out_image, out_transform = mask(src, geoms, crop=True)
    out_meta = src.meta.copy()

    # Save the resulting raster
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    with rasterio.open(file_name, "w", **out_meta) as dest:
        dest.write(out_image)

def raster_to_xyz(raster, csv):

    input_raster = raster
    out_csv = csv

    rtxyz = Raster2xyz()
    rtxyz.translate(input_raster, out_csv)

def plotter(result):

    # Create a plotter window
    plt = Plotter(axes=dict(xtitle='km', ytitle=' ', ztitle='km*1.5', yzGrid=False),
                  size=(1200, 900))  # screen size

    printc("...analyzing...", invert=1)

    # perform a 2D Delaunay triangulation to get the cells from the point cloud
    tri = Delaunay(result.values[:, 0:2])

    # create a mesh object for the land surface
    build = Mesh([result.values, tri.simplices])

    zvals = build.points()[:, 2]

    build.pointColors(zvals, cmap="terrain", vmin=1000)
    build.name = "DTM"  # give the object a name

    return build


def main():
    user_input = input("Enter an adress: ")
    coord = adress_to_location(user_input)
    x2, y2 = proj(coord)
    path = setting_path()
    choosen_path = selecting_path(path, coord)
    rasteriser(x2, y2, choosen_path, "Path_DSM", "cropped_dsm.tif")
    rasteriser(x2, y2, choosen_path, "Path_DTM", "cropped_dtm.tif")
    raster_to_xyz("cropped_dsm.tif", "out_dsm_csv")
    raster_to_xyz("cropped_dtm.tif", "out_dtm_csv")
    result_dsm = pd.read_csv("out_dsm_csv")
    result_dtm = pd.read_csv("out_dtm_csv")
    dsm_build = plotter(result_dsm)
    dtm_build = plotter(result_dtm)
    plt = Plotter(axes=dict(xtitle='km', ytitle=' ', ztitle='km*1.5', yzGrid=False),
                  size=(1200, 900))  # screen size
    plt += dsm_build
    plt += dtm_build
    plt.show(viewup="z")


main()



