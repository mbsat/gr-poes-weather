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

#ifndef INCLUDED_POES_WEATHER_UNIV_HRPT_DEFRAMER_H
#define INCLUDED_POES_WEATHER_UNIV_HRPT_DEFRAMER_H

#include <gr_block.h>

class poesweather_univ_hrpt_deframer;
typedef boost::shared_ptr<poesweather_univ_hrpt_deframer> poesweather_univ_hrpt_deframer_sptr;

poesweather_univ_hrpt_deframer_sptr
poesweather_make_univ_hrpt_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after);

class poesweather_univ_hrpt_deframer : public gr_block
{
  friend poesweather_univ_hrpt_deframer_sptr poesweather_make_univ_hrpt_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after);
  poesweather_univ_hrpt_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after);

  bool               d_sync_check;
  int	             d_frame_length;
  int	     	     d_insync_after;
  int	     	     d_outsync_after;

  bool d_fr_sync;

  unsigned int       d_state;
  bool               d_mid_bit;
  unsigned char      d_last_bit;
  unsigned int       d_bit_count, d_bitcount;
  unsigned int       d_word_count;
  unsigned int       d_sync_marker_count;
  unsigned int       d_nosync_marker_count;
  unsigned long long d_shifter;     // 60 bit sync word
  unsigned short     d_word;        // 10 bit HRPT word
  unsigned int       d_item_count;
  unsigned int       d_framecount;

  void enter_idle();
  void enter_syncing();
  void enter_synced();
  void enter_staysynced();
  void enter_checksync();
 
public:

  void forecast(int noutput_items, gr_vector_int &ninput_items_required);

  int general_work(int noutput_items,
		   gr_vector_int &ninput_items,
		   gr_vector_const_void_star &input_items,
		   gr_vector_void_star &output_items);
};

#endif /* INCLUDED_POES_WEATHER_UNIV_HRPT_DEFRAMER_H */
