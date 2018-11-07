#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from scripts import digital_re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('picp', __name__ ,url_prefix='/picp')

@bp.route('/')
def index():
	print ("进入picp，index()方法")
	return render_template('index.html')
