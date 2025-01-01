import sys
import os

# Stien til din applikationsmappe
sys.path.insert(0, '/home/kaspermu/public_html/Spillerudvikling')

# Aktiver den virtuelle miljø
activate_this = '/home/kaspermu/virtualenv/Spillerudvikling/3.11/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

# Importer din Flask-app
from app import app as application
