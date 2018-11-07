#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
bp = Blueprint('picp', __name__ ,url_prefix='/picp')

@bp.route('/')
def index():
	return render_template('index.html')
#	print ("进入 picp-index ")