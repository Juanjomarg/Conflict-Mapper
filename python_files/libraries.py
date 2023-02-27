#Librerias generales
from datetime import datetime
import os

#Librerias data

import glob
import numpy as np
import pandas as pd
import json
from chardet import detect

#Librerias web

import requests
from bs4 import BeautifulSoup

#Librerias viz

import folium
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

def current_time(request):
  dia=datetime.now().date().day
  mes=datetime.now().date().month
  año=datetime.now().date().year
  if request == 'dia':
      return dia
  if request == 'mes':
      return mes
  if request == 'año':
      return año

def date_today():
  hoy=f"{current_time('dia')}-{current_time('mes')}-{current_time('año')}"
  return hoy

def main():
  pass

###########################################################################
#
#if __name__ == "__main__"
#
###########################################################################

if __name__ == "__main__":
  main()