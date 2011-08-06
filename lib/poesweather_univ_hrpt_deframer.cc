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
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <poesweather_univ_hrpt_deframer.h>
#include <gr_io_signature.h>
#include <poesweather_univ_hrpt.h>
#include <cstring>
#include <cstdio>
#include <iostream>

#define ST_IDLE   0
#define ST_SYNCING 1
#define ST_SYNCED 2
#define ST_CHECK_SYNC 3

using namespace std;

poesweather_univ_hrpt_deframer_sptr
poesweather_make_univ_hrpt_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after)
{
  return gnuradio::get_initial_sptr(new poesweather_univ_hrpt_deframer(sync_check, frame_length, insync_after, outsync_after ));
}

poesweather_univ_hrpt_deframer::poesweather_univ_hrpt_deframer(bool sync_check, int frame_length, int insync_after, int outsync_after)
  : gr_block("poesweather_univ_hrpt_deframer",
	     gr_make_io_signature(1, 1, sizeof(char)),
	     gr_make_io_signature(1, 1, sizeof(short))),
	     d_sync_check(sync_check),
	     d_frame_length(frame_length),
	     d_insync_after(insync_after),
	     d_outsync_after(outsync_after)

{
  //set_output_multiple(SYNC_WORDS); // room for writing full sync when received


  
  d_mid_bit = true;
  d_last_bit = 0;
  enter_idle();
}

void poesweather_univ_hrpt_deframer::forecast(int noutput_items, gr_vector_int &ninput_items_required)
{
   
   ninput_items_required[0] = (noutput_items )*10 *2 ;
}

void
poesweather_univ_hrpt_deframer::enter_idle()
{
  d_state = ST_IDLE;
  d_item_count = 0;
  d_sync_marker_count = 0; 
  d_nosync_marker_count = 0;
}


void
poesweather_univ_hrpt_deframer::enter_syncing()
{
  d_state = ST_SYNCING;
  d_item_count = 0;
  d_shifter=0;
}


void
poesweather_univ_hrpt_deframer::enter_synced()
{
  d_state = ST_SYNCED;
  d_bit_count = BITS_PER_WORD;
  d_word_count = d_frame_length - SYNC_WORDS;
  d_word = 0;
  d_item_count = 0;
}

void
poesweather_univ_hrpt_deframer::enter_staysynced()
{ 
  d_state = ST_SYNCED;
  d_bit_count = BITS_PER_WORD;
  d_word_count = d_frame_length - SYNC_WORDS;
  d_word = 0;
}


void
poesweather_univ_hrpt_deframer::enter_checksync()
{ 
  d_state = ST_CHECK_SYNC;
  d_item_count = 0;
}

int
poesweather_univ_hrpt_deframer::general_work(int noutput_items,
				 gr_vector_int &ninput_items,
				 gr_vector_const_void_star &input_items,
				 gr_vector_void_star &output_items)
{
  int ninputs = ninput_items[0];
  const char *in = (const char *)input_items[0];
  unsigned short *out = (unsigned short *)output_items[0];
  char bit;
  int i = 0, j = 0;

  //while (i < ninputs && j < noutput_items) {
  while (i < ninputs ) {  
    bit = in[i++];

    char diff = bit^d_last_bit;
    d_last_bit = bit;

    //if (d_mid_bit && (diff | (d_state == ST_SYNCED | d_state == ST_CHECK_SYNC) )) {
    if (d_mid_bit && (diff | (d_state == ST_SYNCED | d_state == ST_SYNCING | d_state == ST_CHECK_SYNC) )) {
      switch (d_state) { 
      case ST_IDLE:
	d_shifter = (d_shifter << 1) | bit;   
	d_item_count++;
	if ((d_shifter & 0x0FFFFFFFFFFFFFFFLL) == HRPT_MINOR_FRAME_SYNC) { 
	  d_sync_marker_count++;
          //printf("STATE %i , %i SYNC MARKER FOUND after %i bits \n",d_state, d_sync_marker_count,  d_item_count);
          if (d_sync_marker_count == d_insync_after ) {
            enter_synced();
	  }
	  
          else {
           printf("Deframer : ENTER SYNCING STATE \n"); 
           enter_syncing();
	  }
	}
	break;

      case ST_SYNCING:

       
	  d_shifter = (d_shifter << 1) | bit; 
	  d_item_count++;
		if  (d_item_count == d_frame_length * BITS_PER_WORD) {  
                  d_sync_marker_count++;
		  if((d_shifter & 0x0FFFFFFFFFFFFFFFLL) == HRPT_MINOR_FRAME_SYNC) {
                    
	            //printf("STATE %i , Sync marker nr %i found \n", d_state, d_sync_marker_count);
                    d_item_count = 0;
		    if (d_sync_marker_count == d_insync_after ) {
                      enter_synced(); 
		      printf("Deframer : ENTER SYNCED STATE by %i sync marker \n", d_sync_marker_count);
          	      out[j++] = HRPT_SYNC1;
          	      out[j++] = HRPT_SYNC2;
          	      out[j++] = HRPT_SYNC3;
          	      out[j++] = HRPT_SYNC4;
          	      out[j++] = HRPT_SYNC5;
          	      out[j++] = HRPT_SYNC6;
		    }
		  }
		  else{
                    //printf("STATE %i , SYNC marker %i not present or invalid \n", d_state, d_sync_marker_count );
                    printf("Deframer : ENTER IDLE STATE from syncing state \n");                    
                    enter_idle();
		  }
		}
	break;	

      case ST_SYNCED:
        //printf("bit count %i,   word count %i \n",d_bit_count, d_word_count);       
	d_word = (d_word << 1) | bit; 
	if (--d_bit_count == 0) {
	  out[j++] = d_word;
	  d_word = 0;
	  d_bit_count = BITS_PER_WORD;
	  if (--d_word_count == 0) {
            if (d_sync_check) {
              //printf("ST SYNCED , ENTER CHECK SYNC STATE \n");
              enter_checksync();
	    }
	    else
	    {
              //printf("ST SYNCED , ENTER STAY SYNCED STATE \n");
	      enter_staysynced();
              d_word_count = d_frame_length; 
	    }
	  }
	}
	break;

      case ST_CHECK_SYNC:	
	d_shifter = (d_shifter << 1) | bit;  
	d_item_count++;
	  if (d_item_count == SYNC_WORDS *BITS_PER_WORD ) {
            d_item_count = 0;
	    if ((d_shifter & 0x0FFFFFFFFFFFFFFFLL) == HRPT_MINOR_FRAME_SYNC) {
              //printf("STATE %i , CHECK SYNC, SYNC MARKER VALID\n", d_state);
              d_nosync_marker_count = 0;
              out[j++] = HRPT_SYNC1;
              out[j++] = HRPT_SYNC2;
              out[j++] = HRPT_SYNC3;
              out[j++] = HRPT_SYNC4;
              out[j++] = HRPT_SYNC5;
              out[j++] = HRPT_SYNC6; 
              //printf("ST CHECK SYNC , ENTER STAY SYNCED STATE \n");
              enter_staysynced();
	    }
	    else{
              d_nosync_marker_count++;
	      if (d_nosync_marker_count == d_outsync_after){
                printf("Deframer : ENTER IDLE STATE from check sync state \n");
		enter_idle();
	      }
              else {
                out[j++] = HRPT_SYNC1;
                out[j++] = HRPT_SYNC2;
                out[j++] = HRPT_SYNC3;
                out[j++] = HRPT_SYNC4;
                out[j++] = HRPT_SYNC5;
                out[j++] = HRPT_SYNC6; 

                enter_staysynced();
                //printf("STATE %i , CHECK SYNC, SYNC MARKER %i from max %i is INVALID !!!!!!!\n", d_state, d_nosync_marker_count, d_outsync_after );
              }
	    }
	  }		
        
	break;
	
      default:
	throw std::runtime_error("poesweather_univ_hrpt_deframer: bad state\n");
      }

      d_mid_bit = false;
    }
    else {
      d_mid_bit = true;
    }
  }
  //printf("We have %i input, %i output items, loops %i, returned j %i \n", ninputs, noutput_items, i, j);
  consume_each(i);
  return j;
}
