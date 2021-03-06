#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import struct
import numpy
import os

from funciones   import ymd
from os.path     import basename
from color_array import colorArray
from mpl_toolkits.basemap import Basemap

def rangoColorbar(band):

  # defino los rangos del colorbar en funcion del tipo de banda
  if band == 'FR' or band == 'RP':
    vmin = 0
    vmax = 100
  elif band == 'T2':
    vmin = -70
    vmax = 70
  elif band == 'T3':
    vmin = -100
    vmax = 30
  elif band == 'T4':
    vmin = -80
    vmax = 70
  elif band == 'T6':
    vmin = -100
    vmax = 70

  return vmin, vmax

# rangoColorbar

#########################################
#########################################
#########################################

def bandTag(banda):

  if banda == 'FR':
    return "CH1 FR"
  elif banda == 'RP':
    return "CH1 RP"
  elif banda == 'T2':
    return "CH2 T2"
  elif banda == 'T3':
    return "CH3 T3"
  elif banda == 'T4':
    return "CH4 T4"
  elif banda == 'T6':
    return "CH6 T6"

# bandTag

#########################################
#########################################
#########################################

def getExt(url):
  name = basename(url)
  return name.split('.')[-1]
# getExt

#########################################
#########################################
#########################################

def getFolderExt(banda):

  if banda == 'FR':
    return "B01-FR"
  elif banda == 'RP':
    return "B01-RP"
  elif banda == 'T2':
    return "B02"
  elif banda == 'T3':
    return "B03"
  elif banda == 'T4':
    return "B04"
  elif banda == 'T6':
    return "B06"

# getFolderExt

#########################################
#########################################
#########################################

def getBandlabel(band):
  if band == 'FR':
    return "Factor de reflectancia (%)"
  elif band == 'RP':
    return "Reflectancia planetaria (%)"
  else:
    return "Temperatura de brillo ($^\circ$C)"
# getBandlabel

#########################################
#########################################
#########################################

'''
Ésta función genera el tag que se utiliza como pie de página
de la imágen generada.
Ejemplo: CH3 T3 11-10-2016 13:35 UTC
'''

def nameTag(basename):
  name       = basename[:-3]
  name_split = name.split("_")
  year       = name_split[1][0:4]
  doy        = name_split[1][4:8]
  hms        = name_split[2]
  month      = ymd(int(year), int(doy))[1]
  day        = ymd(int(year), int(doy))[2]

  str_day   = str(day).zfill(2)
  str_month = str(month).zfill(2)
  str_hm    = hms[0:2] + ":" +hms[2:4]
  str_chnl  = bandTag(getExt(basename))

  return str_chnl + " " + str_day + "-" + str_month + "-" + year + " " + str_hm + " UTC"  
# nameTag

#########################################
#########################################
#########################################

def setcolor(x, color):
  for m in x:
    for t in x[m][1]:
      t.set_color(color)

#########################################
#########################################
#########################################

def fileToPng(file, metaPath, outPngPath):

  # abro el archivo meta y guardo los datos
  fid = open(metaPath + '/T000gri.META', 'r')
  meta = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # abro el archivo T000gri.LATvec y guardo los datos
  fid = open(metaPath + '/T000gri.LATvec', 'r')
  LATdeg_vec = numpy.fromfile(fid, dtype='float32')
  LATdeg_vec = LATdeg_vec[::-1] # invierto el arreglo porque quedaba invertido verticalmente
  fid.close()

  # abro el archivo T000gri.LONvec y guardo los datos
  fid = open(metaPath + '/T000gri.LONvec', 'r')
  LONdeg_vec = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # obtengo del vector meta el largo y alto de elementos de los vectores y los datos
  Ci = meta[0];
  Cj = meta[1];
  Ct = Ci*Cj;

  # con esto quito el formato de escritura de numeracion cientifica
  # numpy.set_printoptions(suppress=True)

  # print file
  # print meta
  # print Ci
  # print Cj
  # print Ct
  # print LATdeg_vec.size
  # print LATdeg_vec.size

  min_lon = numpy.amin(LONdeg_vec)
  max_lon = numpy.amax(LONdeg_vec)
  min_lat = numpy.amin(LATdeg_vec)
  max_lat = numpy.amax(LATdeg_vec)

  print "Lon min:" + str(min_lon) + ", Lon max:" + str(max_lon)
  print "Lat min:" + str(min_lat) + ", Lat max:" + str(max_lat)

  # seteo los minimos y maximos de la imagen en funcion de los min y max de lat y long
  axes = plt.gca()
  axes.set_xlim([min_lon, max_lon])
  axes.set_ylim([min_lat, max_lat])

  # abro el archivo file y lo guardo en data
  fid  = open(file, 'r')
  data = numpy.fromfile(fid, dtype='float32')
  fid.close()

  # paso el vector data a una matriz de tamano Ci Cj
  IMG = numpy.reshape(data, (Ci, Cj))

  # genero un mapa con la proyecccion de mercator y lat y lons los anteriores
  ax = Basemap(projection='merc',\
                llcrnrlat=min_lat,urcrnrlat=max_lat,\
                llcrnrlon=min_lon,urcrnrlon=max_lon,\
                resolution='l')

  # dibujo las costas, estados y paises
  ax.drawcoastlines()
  ax.drawstates()
  ax.drawcountries()

  # dibujo los valores de latitudes y longitudes al margen de la imagen
  par = ax.drawparallels(numpy.arange(-45, -20, 5), labels=[1,0,0,0], linewidth=0.0, fontsize=10, color='white')
  mer = ax.drawmeridians(numpy.arange(-70, -45, 5), labels=[0,0,1,0], linewidth=0.0, fontsize=10, color='white')

  setcolor(par,'white')
  setcolor(mer,'white')

  # genero un meshgrid a partir de LonVec y LatVec
  lons2d, lats2d = numpy.meshgrid(LONdeg_vec, LATdeg_vec)
  # y luego obtengo sus coordenadas en el mapa ax
  x, y = ax(lons2d,lats2d)

  # Dibujo Estacion LES
  les_lon = -57.92
  les_lat = -31.28
  les_x, les_y = ax(les_lon, les_lat)
  print les_x
  print les_y
  ax.plot(les_x, les_y, 'bo', markersize=0.1, linewidth=0.0, color='white')

  # obtengo la extension del archivo para mapear la banda
  band = getExt(file)

  # defino el min y max en funcion de la banda
  vmin, vmax = rangoColorbar(band)

  # defino el colormap  y la disposicion de los ticks segun la banda
  if band == 'FR' or band == 'RP':
    cmap        = 'jet'
    ticks       = [0, 20, 40, 60, 80, 100]
    ticksLabels = ticks
  elif band == 'T4':

    # Los datos de T2 a T6 estan en kelvin, asi que los paso a Celsius
    IMG  -= 273.15
    cmap  = colorArray(1024, vmin, vmax)

    ticks = [-80, -75.2, -70.2, -65.2, -60.2, -55.2, -50.2, -45.2, -40.2, -35.2, -30.2,-20,-10,0,10,20,30,40,50,60,70]
    # defino las etiquetas del colorbar
    ticksLabels = [-80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30,-20,-10,0,10,20,30,40,50,60,70]
  else:
    # Los datos de T2 a T6 estan en kelvin, asi que los paso a Celsius
    IMG        -= 273.15
    cmap        = 'gray_r'
    ticks       = numpy.arange(vmin,vmax+10,10)
    ticksLabels = ticks
  # if FR o RP

  # print "MAX: " + str(numpy.amax(IMG))
  # print "MIN: " + str(numpy.amin(IMG))

  # grafico IMG1 usando lon como vector x y lat como vector y
  cs = ax.pcolormesh(x, y, IMG, vmin=vmin, vmax=vmax, cmap=cmap)

  # seteo los limites del colorbar
  plt.clim(vmin, vmax)

  # agrego el colorbar
  cbar = ax.colorbar(cs, location='bottom', pad='3%', ticks=ticks)

  if band == 'T4':
    cbar.ax.set_xticklabels(ticksLabels, rotation=45, fontsize=7, color='white')
  else:
    cbar.ax.set_xticklabels(ticksLabels, fontsize=7, color='white')

  cbar.ax.set_xlabel(getBandlabel(band), fontsize=7, color='white')

  if band == 'T4':
    cbar.ax.xaxis.labelpad = 0

  # agrego el logo en el documento
  logo = plt.imread('/sat/PRS/libs/PRS-sat/PRSpng/imgs/les_191_bw.png')
  plt.figimage(logo, 5, 5)

  # genero los datos para escribir el pie de pagina
  name = basename(file)           # obtengo el nombre base del archivo
  year = name[4:8]

  # chequeo existsencia de ruta final y directorios intermedios, sino los creo
  bandFolder = getFolderExt(band)

  # si no existe la carpeta asociada a la banda la creo
  if not os.path.isdir(outPngPath + bandFolder):
    os.mkdir(outPngPath + bandFolder)
  # if

  # si no existe la carpeta asociada al ano la creo
  if not os.path.isdir(outPngPath + bandFolder + '/' + str(year)):
    os.mkdir(outPngPath + bandFolder + "/" + str(year))
  # if

  outPath = outPngPath + bandFolder + "/" + str(year) + "/"

  destFile = outPath + name[0:18] + '.png' # genero la ruta y nombre del archivo a guardar

  tag = nameTag(name)

  # si todas las entradas del vector data son cero, entonces es noche y agrego el texto NOCHE
  if numpy.sum(data) == 0.:
    plt.annotate("NOCHE", (0,0), (245, 15), color='white', xycoords='axes fraction', textcoords='offset points', va='top', fontsize=10, family='monospace')
    # print "es noche"

  # genero el pie de la imagen, con el logo y la info del archivo
  plt.annotate(tag, (0,0), (80, -60), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=14, family='monospace', color='white')

  # guardo la imagen en la ruta destino
  plt.savefig(destFile, bbox_inches='tight', dpi=200, transparent=True)
  plt.savefig(destFile, bbox_inches='tight', dpi=200, transparent=True)
  plt.close() # cierro el archivo

# fileToPng
