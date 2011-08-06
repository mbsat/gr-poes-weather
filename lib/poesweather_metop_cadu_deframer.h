/* -*- c++ -*- */
/*
 * Copyright 2009 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 *  
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option) 
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful, 
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License 
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA. 
 */

#ifndef INCLUDED_POES_WEATHER_METOP_CADU_DEFRAMER_H
#define INCLUDED_POES_WEATHER_METOP_CADU_DEFRAMER_H

#include <gr_block.h>

class poesweather_metop_cadu_deframer;
typedef boost::shared_ptr<poesweather_metop_cadu_deframer> poesweather_metop_cadu_deframer_sptr;

poesweather_metop_cadu_deframer_sptr
poesweather_make_metop_cadu_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after);

class poesweather_metop_cadu_deframer : public gr_block
{
  friend poesweather_metop_cadu_deframer_sptr poesweather_make_metop_cadu_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after);
  poesweather_metop_cadu_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after);

  bool               d_sync_check;
  int	             d_frame_length;
  int	     	     d_insync_after;
  int	     	     d_outsync_after;



  unsigned int       d_state;
  unsigned int       d_bit_count;
  unsigned int       d_word_count;
  unsigned int       d_sync_marker_count;
  unsigned int       d_nosync_marker_count;
  unsigned long      d_shifter;     
  unsigned char      d_word;        
  unsigned int       d_item_count;
  unsigned int       d_framecount;
  bool 		     d_negative;


  void enter_idle();
  void enter_syncing();
  void enter_synced();
  void enter_staysynced();
  void enter_checksync();
 
public:
  int general_work(int noutput_items,
		   gr_vector_int &ninput_items,
		   gr_vector_const_void_star &input_items,
		   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_POES_WEATHER_METOP_CADU_DEFRAMER_H */
