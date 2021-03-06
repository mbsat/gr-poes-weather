/*
 * Copyright 2010 Free Software Foundation, Inc.
 * 
 * This file is part of gr-poes-weather high resolution
 * satellite imagery signal processing package.
 * 
 * POES-Weather Ltd
 * http://www.poes-weather.com
 *
 * gr-poes-weather is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * gr-poes-weather is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

%include "gnuradio.i"

%{
#include <poesweather_noaa_hrpt_deframer.h>
#include <poesweather_mn1_hrpt_deframer.h>
#include <poesweather_fy1_hrpt_deframer.h>
#include <poesweather_fy1_hrpt_decoder.h>
#include <poesweather_metop_cadu_deframer.h>
#include <poesweather_meteor_cadu_deframer.h>
#include <poesweather_univ_hrpt_deframer.h>
#include <poesweather_metop_cadu_defraderan.h>
%}

%include "poesweather_noaa_hrpt_deframer.i"
%include "poesweather_mn1_hrpt_deframer.i"
%include "poesweather_fy1_hrpt_deframer.i"
%include "poesweather_fy1_hrpt_decoder.i"
%include "poesweather_metop_cadu_deframer.i"
%include "poesweather_meteor_cadu_deframer.i"
%include "poesweather_univ_hrpt_deframer.i"
%include "poesweather_metop_cadu_defraderan.i"

