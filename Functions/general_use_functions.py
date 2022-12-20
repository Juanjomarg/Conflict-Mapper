#Librerias generales
import sys
from datetime import *
from random import *
import os
import platform
import logging as _logging
import time
from threading import *

#Librerias data

import glob
from unicodedata import name
import numpy as np
import pandas as pd
import json

#Librerias web

import requests
import bs4 as bs
import feedparser
from cefpython3 import cefpython as cef

#Librerias geo

from geopy import *
import geopandas as gpd
from geopandas import tools
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry import Point
import folium

#Librerias viz

import matplotlib
import plotly
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ctypes

###########################################################################
#
#Tiempo
#
###########################################################################

def fecha_actual(request):
  dia=datetime.now().date().day
  mes=datetime.now().date().month
  año=datetime.now().date().year
  if request == 'dia':
      return dia
  if request == 'mes':
      return mes
  if request == 'año':
      return año

def fecha_hoy():
  hoy=f"{fecha_actual('dia')}-{fecha_actual('mes')}-{fecha_actual('año')}"
  return hoy

###########################################################################
#
#Carga de archivos
#
###########################################################################

def cargar_ciudades():
  ciudades_df=pd.read_csv(fr'./Infraestructura/CSV/Ciudades.csv',index_col=0)
  return ciudades_df

def cargar_aeropuertos():
  aeropuertos_df=pd.read_csv(fr'./Infraestructura/CSV/Aeropuertos.csv',index_col=0)
  return aeropuertos_df

def cargar_noticias():
  noticias=pd.read_csv(fr'./RSS/NEWS_CSV/NewsCSV.csv')
  return noticias

def main():
  pass

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

if __name__ == "__main__":
  main()