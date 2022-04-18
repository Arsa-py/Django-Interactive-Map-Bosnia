from unicodedata import name
from django.shortcuts import render, redirect
import os
import folium

# Create your views here.

def home(request):
    context = {}
    return render(request, 'geoApp/home.html', context)


def gismap(request):
    shp_dir = os.path.join(os.getcwd(), 'media', 'shp')

    # Folium
    m = folium.Map(location=[43.9165389, 17.6721508], zoom_start=8, prefer_canvas=True)

    # Style
    style_caves = {'fillColor': '#228B22', 'color': '#228B22'}
    style_emerald_network = { 'fillColor': 'green', 'color': 'green', 'weight': 5, 'fillOpacity': 0.5}
    style_watersheds = {'color': 'aqua', 'weight': 5}
    style_water_areas = {'fillColor': 'blue', 'color': 'blue', 'weight': 5, 'fillOpacity': 0.5}
    style_water_lines = {'color': 'blue', 'weight': 5}
    style_healthsites = {'fillColor': 'red', 'color': 'red', 'weight': 5, 'fillOpacity': 0.5}
    style_BIH_ADM0 = {'fillColor': 'yellow', 'color': 'yellow', 'fillOpacity': 0.3}
    style_BIH_ADM1 = {'fillColor': 'orange', 'color': 'orange', 'fillOpacity': 0.3}
    style_BIH_ADM2 = {'fillColor': 'purple', 'color': 'purple', 'fillOpacity': 0.3}


    folium.GeoJson(os.path.join(shp_dir,'caves.geojson'), name='Pećine', 
                            style_function=lambda x: style_caves, 
                            popup=folium.features.GeoJsonPopup(fields=['Name'], localize=True)).add_to(m).show=False

    folium.GeoJson(os.path.join(shp_dir, 'emerald_network.geojson'), name='Smaragdne Mreže', 
                                style_function=lambda x:style_emerald_network, 
                                popup=folium.features.GeoJsonPopup(fields=['Site_name'], localize=True)).add_to(m).show=False

    folium.GeoJson(os.path.join(shp_dir, 'water_areas.json'), name='Vodene Površine', 
                                style_function=lambda x:style_water_areas, 
                                popup=folium.features.GeoJsonPopup(fields=['NAME'], localize=True)).add_to(m).show=False

    # Doesn't show much data on a map
    # folium.GeoJson(os.path.join(shp_dir, 'water_lines.json'), name='Vodene Linije', 
    #                             style_function=lambda x:style_water_lines, 
    #                             popup=folium.features.GeoJsonPopup(fields=['NAME'], localize=True)).add_to(m).show=False

    # Shows much more data on a map
    folium.GeoJson(open('media/shp/waterways.json', encoding='utf-8-sig').read(), name='Vodene Linije', 
                                 style_function=lambda x:style_water_lines, 
                                 popup=folium.features.GeoJsonPopup(fields=['name'], localize=True)).add_to(m).show=False

    folium.GeoJson(os.path.join(shp_dir, 'watersheds.geojson'), name='Slivovi', 
                                style_function=lambda x:style_watersheds,
                                popup=folium.features.GeoJsonPopup(fields=['Basin'], localize=True)).add_to(m).show=False

    folium.GeoJson(os.path.join(shp_dir, 'healthsites.geojson'), name='Zdravstvene ustanove', 
                    style_function=lambda x:style_healthsites,
                    popup=folium.features.GeoJsonPopup(fields=['name', 'amenity'], localize=True)).add_to(m).show=False

    folium.GeoJson(os.path.join(shp_dir, 'geoBoundaries-BIH-ADM0.geojson'), name='BIH Adm Granice I', 
                    style_function=lambda x:style_BIH_ADM0,
                    popup=folium.features.GeoJsonPopup(fields=['shapeName'], localize=True)).add_to(m).show=False
    
    folium.GeoJson(os.path.join(shp_dir, 'geoBoundaries-BIH-ADM1.geojson'), name='BIH Adm Granice II', 
                    style_function=lambda x:style_BIH_ADM1,
                    popup=folium.features.GeoJsonPopup(fields=['shapeName'], localize=True)).add_to(m).show=False

    folium.GeoJson(open('media/shp/geoBoundaries-BIH-ADM2.geojson', encoding='utf-8-sig').read(), name='BIH Adm Granice III', 
                     style_function=lambda x:style_BIH_ADM2,
                     popup=folium.features.GeoJsonPopup(fields=['shapeName'], localize=True)).add_to(m).show=False


    # Folium Tile Layer
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)

    folium.LayerControl().add_to(m)
    # folium.LatLngPopup().add_to(m)
    
    # Exporting
    m = m._repr_html_()
    context = {
        'my_map': m,
        'name': 'NAME',
    }

    # Rendering
    return render(request, 'geoApp/gismap.html', context)