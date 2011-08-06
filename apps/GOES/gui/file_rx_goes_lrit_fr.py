#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: LRIT Receiver from baseband file
# Author: Martin Blaho
# Description: GOES - LRIT receive and decode signal to CADU -use baseband file as input
# Generated: Thu Jan 13 20:44:54 2011
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from time import strftime, localtime, gmtime
import fec
import math, os
import poesweather
import wx

class file_rx_goes_lrit_fr(grc_wxgui.top_block_gui):

	def __init__(self, deframer_insync_frames=2, viterbi_insync_frames=5, deframer_outsync_frames=5, viterbi_outsync_frames=20, viterbi_sync_check=True, viterbi_sync_threshold=0.1, deframer_sync_check=True, clock_alpha=0.005, symb_rate=293883, pll_alpha=0.005, satellite='GOES-LRIT', freq=1691.02e6, gain=23, decim=108, side="A", frames_file=os.environ['HOME'] + '/GOES-LRIT_cadu_frames.cadu', baseband_file=os.environ['HOME'] + '/GOES-LRIT_baseband.dat'):
		grc_wxgui.top_block_gui.__init__(self, title="LRIT Receiver from baseband file")

		##################################################
		# Parameters
		##################################################
		self.deframer_insync_frames = deframer_insync_frames
		self.viterbi_insync_frames = viterbi_insync_frames
		self.deframer_outsync_frames = deframer_outsync_frames
		self.viterbi_outsync_frames = viterbi_outsync_frames
		self.viterbi_sync_check = viterbi_sync_check
		self.viterbi_sync_threshold = viterbi_sync_threshold
		self.deframer_sync_check = deframer_sync_check
		self.clock_alpha = clock_alpha
		self.symb_rate = symb_rate
		self.pll_alpha = pll_alpha
		self.satellite = satellite
		self.freq = freq
		self.gain = gain
		self.decim = decim
		self.side = side
		self.frames_file = frames_file
		self.baseband_file = baseband_file

		##################################################
		# Variables
		##################################################
		self.decim_tb = decim_tb = decim
		self.symb_rate_tb = symb_rate_tb = symb_rate
		self.samp_rate = samp_rate = 64e6/decim_tb
		self.viterbi_sync_threshold_text = viterbi_sync_threshold_text = viterbi_sync_threshold
		self.viterbi_sync_after_text = viterbi_sync_after_text = viterbi_insync_frames
		self.viterbi_outofsync_after_text = viterbi_outofsync_after_text = viterbi_outsync_frames
		self.viterbi_node_sync_text = viterbi_node_sync_text = viterbi_sync_check
		self.sps = sps = samp_rate/symb_rate_tb
		self.satellite_text = satellite_text = satellite
		self.samp_rate_st = samp_rate_st = samp_rate
		self.pll_alpha_sl = pll_alpha_sl = pll_alpha
		self.gain_tb = gain_tb = gain
		self.freq_tb = freq_tb = freq
		self.frames_file_text_inf = frames_file_text_inf = frames_file
		self.deframer_sync_after_text = deframer_sync_after_text = deframer_insync_frames
		self.deframer_nosync_after_text = deframer_nosync_after_text = deframer_outsync_frames
		self.deframer_check_sync_text = deframer_check_sync_text = deframer_sync_check
		self.datetime_text = datetime_text = strftime("%A, %B %d %Y %H:%M:%S", localtime())
		self.clock_alpha_sl = clock_alpha_sl = clock_alpha
		self.baseband_file_text_inf = baseband_file_text_inf = 'no output file'

		##################################################
		# Notebooks
		##################################################
		self.rx_ntb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "USRP Receiver")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "PLL demodulator and Clock sync")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Viterbi decoder")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Deframer")
		self.rx_ntb.AddPage(grc_wxgui.Panel(self.rx_ntb), "Output")
		self.Add(self.rx_ntb)

		##################################################
		# Controls
		##################################################
		self._decim_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.decim_tb,
			callback=self.set_decim_tb,
			label="Decimation",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._decim_tb_text_box, 1, 3, 1, 1)
		self._symb_rate_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			value=self.symb_rate_tb,
			callback=self.set_symb_rate_tb,
			label="Symbol rate",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(1).GridAdd(self._symb_rate_tb_text_box, 2, 1, 1, 1)
		self._viterbi_sync_threshold_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.viterbi_sync_threshold_text,
			callback=self.set_viterbi_sync_threshold_text,
			label="Viterbi node sync threshold [BER]",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._viterbi_sync_threshold_text_static_text, 3, 0, 1, 1)
		self._viterbi_sync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.viterbi_sync_after_text,
			callback=self.set_viterbi_sync_after_text,
			label="Valid frames for Viterbi decoder sync",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._viterbi_sync_after_text_static_text, 4, 0, 1, 1)
		self._viterbi_outofsync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.viterbi_outofsync_after_text,
			callback=self.set_viterbi_outofsync_after_text,
			label="Invalid frames for Viterbi decoder out of sync",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._viterbi_outofsync_after_text_static_text, 5, 0, 1, 1)
		self._viterbi_node_sync_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(2).GetWin(),
			value=self.viterbi_node_sync_text,
			callback=self.set_viterbi_node_sync_text,
			label="Viterbi node sync enable",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(2).GridAdd(self._viterbi_node_sync_text_static_text, 2, 0, 1, 1)
		self._satellite_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.satellite_text,
			callback=self.set_satellite_text,
			label="Sat ",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._satellite_text_static_text, 1, 0, 1, 1)
		self._samp_rate_st_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.samp_rate_st,
			callback=self.set_samp_rate_st,
			label="Sample rate",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._samp_rate_st_static_text, 1, 4, 1, 1)
		_pll_alpha_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._pll_alpha_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_alpha_sl_sizer,
			value=self.pll_alpha_sl,
			callback=self.set_pll_alpha_sl,
			label="PLL Alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._pll_alpha_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_pll_alpha_sl_sizer,
			value=self.pll_alpha_sl,
			callback=self.set_pll_alpha_sl,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_pll_alpha_sl_sizer, 1, 0, 1, 1)
		self._gain_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.gain_tb,
			callback=self.set_gain_tb,
			label="RX gain [dB]",
			converter=forms.int_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._gain_tb_text_box, 1, 2, 1, 1)
		self._freq_tb_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(0).GetWin(),
			value=self.freq_tb,
			callback=self.set_freq_tb,
			label="Frequency",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(0).GridAdd(self._freq_tb_text_box, 1, 1, 1, 1)
		self._frames_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(4).GetWin(),
			value=self.frames_file_text_inf,
			callback=self.set_frames_file_text_inf,
			label="Frames filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(4).GridAdd(self._frames_file_text_inf_static_text, 3, 0, 1, 1)
		self._deframer_sync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.deframer_sync_after_text,
			callback=self.set_deframer_sync_after_text,
			label="Deframe sync after",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._deframer_sync_after_text_static_text, 3, 0, 1, 1)
		self._deframer_nosync_after_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.deframer_nosync_after_text,
			callback=self.set_deframer_nosync_after_text,
			label="Deframer out of sync after",
			converter=forms.float_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._deframer_nosync_after_text_static_text, 4, 0, 1, 1)
		self._deframer_check_sync_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(3).GetWin(),
			value=self.deframer_check_sync_text,
			callback=self.set_deframer_check_sync_text,
			label="Deframer check sync enable",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(3).GridAdd(self._deframer_check_sync_text_static_text, 2, 0, 1, 1)
		self._datetime_text_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(4).GetWin(),
			value=self.datetime_text,
			callback=self.set_datetime_text,
			label="Local time of aquisition start",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(4).GridAdd(self._datetime_text_static_text, 1, 0, 1, 1)
		_clock_alpha_sl_sizer = wx.BoxSizer(wx.VERTICAL)
		self._clock_alpha_sl_text_box = forms.text_box(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_clock_alpha_sl_sizer,
			value=self.clock_alpha_sl,
			callback=self.set_clock_alpha_sl,
			label="Clock alpha",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._clock_alpha_sl_slider = forms.slider(
			parent=self.rx_ntb.GetPage(1).GetWin(),
			sizer=_clock_alpha_sl_sizer,
			value=self.clock_alpha_sl,
			callback=self.set_clock_alpha_sl,
			minimum=0.001,
			maximum=0.1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.rx_ntb.GetPage(1).GridAdd(_clock_alpha_sl_sizer, 1, 1, 1, 1)
		self._baseband_file_text_inf_static_text = forms.static_text(
			parent=self.rx_ntb.GetPage(4).GetWin(),
			value=self.baseband_file_text_inf,
			callback=self.set_baseband_file_text_inf,
			label="Baseband filename",
			converter=forms.str_converter(),
		)
		self.rx_ntb.GetPage(4).GridAdd(self._baseband_file_text_inf_static_text, 4, 0, 1, 1)

		##################################################
		# Blocks
		##################################################
		self.fec_decode_viterbi_bpsk_fb_0 = fec.decode_viterbi_bpsk_fb(viterbi_sync_check, viterbi_sync_threshold, viterbi_insync_frames, viterbi_outsync_frames, viterbi_outsync_frames*3)
		self.gr_agc_xx_0 = gr.agc_cc(10e-6, 1, 1.0/32767.0, 1.0)
		self.gr_clock_recovery_mm_xx_0 = gr.clock_recovery_mm_cc(sps, clock_alpha_sl*clock_alpha_sl/4.0, 0.5, clock_alpha_sl, 0.05)
		self.gr_complex_to_real_0 = gr.complex_to_real(1)
		self.gr_costas_loop_cc_0 = gr.costas_loop_cc(pll_alpha_sl, pll_alpha_sl*pll_alpha_sl/4.0, 0.07, -0.07, 2)
		self.gr_file_source_0 = gr.file_source(gr.sizeof_gr_complex*1, "/home/martin/GNURadioData/lrit/goes_lrit_D108AD64MHz.sam", True)
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vcc((1, ))
		self.gr_null_sink_0 = gr.null_sink(gr.sizeof_char*1)
		self.gr_packed_to_unpacked_xx_0 = gr.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
		self.gr_throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.poesweather_metop_cadu_deframer_0 = poesweather.metop_cadu_deframer(True, 1024, deframer_insync_frames, deframer_outsync_frames)
		self.root_raised_cosine_filter_0 = gr.fir_filter_ccf(1, firdes.root_raised_cosine(
			1, samp_rate, symb_rate, 0.25, int(11*samp_rate/symb_rate)))
		self.wxgui_fftsink1 = fftsink2.fft_sink_c(
			self.rx_ntb.GetPage(0).GetWin(),
			baseband_freq=freq,
			y_per_div=2,
			y_divs=10,
			ref_level=12,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="Not filtered spectrum",
			peak_hold=False,
		)
		self.rx_ntb.GetPage(0).Add(self.wxgui_fftsink1.win)
		self.wxgui_fftsink2 = fftsink2.fft_sink_c(
			self.rx_ntb.GetPage(0).GetWin(),
			baseband_freq=0,
			y_per_div=2,
			y_divs=10,
			ref_level=12,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="RRC filtered spectrum",
			peak_hold=False,
		)
		self.rx_ntb.GetPage(0).Add(self.wxgui_fftsink2.win)
		self.wxgui_scopesink2_1 = scopesink2.scope_sink_c(
			self.rx_ntb.GetPage(1).GetWin(),
			title="BPSK constellation diagram",
			sample_rate=symb_rate,
			v_scale=0.4,
			v_offset=0,
			t_scale=1/samp_rate,
			ac_couple=False,
			xy_mode=True,
			num_inputs=1,
		)
		self.rx_ntb.GetPage(1).Add(self.wxgui_scopesink2_1.win)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_agc_xx_0, 0), (self.root_raised_cosine_filter_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_complex_to_real_0, 0))
		self.connect((self.fec_decode_viterbi_bpsk_fb_0, 0), (self.gr_packed_to_unpacked_xx_0, 0))
		self.connect((self.gr_packed_to_unpacked_xx_0, 0), (self.poesweather_metop_cadu_deframer_0, 0))
		self.connect((self.gr_complex_to_real_0, 0), (self.fec_decode_viterbi_bpsk_fb_0, 0))
		self.connect((self.gr_clock_recovery_mm_xx_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.gr_costas_loop_cc_0, 0), (self.gr_clock_recovery_mm_xx_0, 0))
		self.connect((self.root_raised_cosine_filter_0, 0), (self.gr_costas_loop_cc_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_1, 0))
		self.connect((self.root_raised_cosine_filter_0, 0), (self.wxgui_fftsink2, 0))
		self.connect((self.gr_agc_xx_0, 0), (self.wxgui_fftsink1, 0))
		self.connect((self.poesweather_metop_cadu_deframer_0, 0), (self.gr_null_sink_0, 0))
		self.connect((self.gr_throttle_0, 0), (self.gr_agc_xx_0, 0))
		self.connect((self.gr_file_source_0, 0), (self.gr_throttle_0, 0))

	def set_deframer_insync_frames(self, deframer_insync_frames):
		self.deframer_insync_frames = deframer_insync_frames
		self.set_deframer_sync_after_text(self.deframer_insync_frames)

	def set_viterbi_insync_frames(self, viterbi_insync_frames):
		self.viterbi_insync_frames = viterbi_insync_frames
		self.set_viterbi_sync_after_text(self.viterbi_insync_frames)

	def set_deframer_outsync_frames(self, deframer_outsync_frames):
		self.deframer_outsync_frames = deframer_outsync_frames
		self.set_deframer_nosync_after_text(self.deframer_outsync_frames)

	def set_viterbi_outsync_frames(self, viterbi_outsync_frames):
		self.viterbi_outsync_frames = viterbi_outsync_frames
		self.set_viterbi_outofsync_after_text(self.viterbi_outsync_frames)

	def set_viterbi_sync_check(self, viterbi_sync_check):
		self.viterbi_sync_check = viterbi_sync_check
		self.set_viterbi_node_sync_text(self.viterbi_sync_check)

	def set_viterbi_sync_threshold(self, viterbi_sync_threshold):
		self.viterbi_sync_threshold = viterbi_sync_threshold
		self.set_viterbi_sync_threshold_text(self.viterbi_sync_threshold)

	def set_deframer_sync_check(self, deframer_sync_check):
		self.deframer_sync_check = deframer_sync_check
		self.set_deframer_check_sync_text(self.deframer_sync_check)

	def set_clock_alpha(self, clock_alpha):
		self.clock_alpha = clock_alpha
		self.set_clock_alpha_sl(self.clock_alpha)

	def set_symb_rate(self, symb_rate):
		self.symb_rate = symb_rate
		self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, 0.25, int(11*self.samp_rate/self.symb_rate)))
		self.set_symb_rate_tb(self.symb_rate)
		self.wxgui_scopesink2_1.set_sample_rate(self.symb_rate)

	def set_pll_alpha(self, pll_alpha):
		self.pll_alpha = pll_alpha
		self.set_pll_alpha_sl(self.pll_alpha)

	def set_satellite(self, satellite):
		self.satellite = satellite
		self.set_satellite_text(self.satellite)

	def set_freq(self, freq):
		self.freq = freq
		self.set_freq_tb(self.freq)
		self.wxgui_fftsink1.set_baseband_freq(self.freq)

	def set_gain(self, gain):
		self.gain = gain
		self.set_gain_tb(self.gain)

	def set_decim(self, decim):
		self.decim = decim
		self.set_decim_tb(self.decim)

	def set_side(self, side):
		self.side = side

	def set_frames_file(self, frames_file):
		self.frames_file = frames_file
		self.set_frames_file_text_inf(self.frames_file)

	def set_baseband_file(self, baseband_file):
		self.baseband_file = baseband_file

	def set_decim_tb(self, decim_tb):
		self.decim_tb = decim_tb
		self.set_samp_rate(64e6/self.decim_tb)
		self._decim_tb_text_box.set_value(self.decim_tb)

	def set_symb_rate_tb(self, symb_rate_tb):
		self.symb_rate_tb = symb_rate_tb
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self._symb_rate_tb_text_box.set_value(self.symb_rate_tb)

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symb_rate, 0.25, int(11*self.samp_rate/self.symb_rate)))
		self.set_samp_rate_st(self.samp_rate)
		self.wxgui_fftsink1.set_sample_rate(self.samp_rate)
		self.set_sps(self.samp_rate/self.symb_rate_tb)
		self.wxgui_fftsink2.set_sample_rate(self.samp_rate)

	def set_viterbi_sync_threshold_text(self, viterbi_sync_threshold_text):
		self.viterbi_sync_threshold_text = viterbi_sync_threshold_text
		self._viterbi_sync_threshold_text_static_text.set_value(self.viterbi_sync_threshold_text)

	def set_viterbi_sync_after_text(self, viterbi_sync_after_text):
		self.viterbi_sync_after_text = viterbi_sync_after_text
		self._viterbi_sync_after_text_static_text.set_value(self.viterbi_sync_after_text)

	def set_viterbi_outofsync_after_text(self, viterbi_outofsync_after_text):
		self.viterbi_outofsync_after_text = viterbi_outofsync_after_text
		self._viterbi_outofsync_after_text_static_text.set_value(self.viterbi_outofsync_after_text)

	def set_viterbi_node_sync_text(self, viterbi_node_sync_text):
		self.viterbi_node_sync_text = viterbi_node_sync_text
		self._viterbi_node_sync_text_static_text.set_value(self.viterbi_node_sync_text)

	def set_sps(self, sps):
		self.sps = sps
		self.gr_clock_recovery_mm_xx_0.set_omega(self.sps)

	def set_satellite_text(self, satellite_text):
		self.satellite_text = satellite_text
		self._satellite_text_static_text.set_value(self.satellite_text)

	def set_samp_rate_st(self, samp_rate_st):
		self.samp_rate_st = samp_rate_st
		self._samp_rate_st_static_text.set_value(self.samp_rate_st)

	def set_pll_alpha_sl(self, pll_alpha_sl):
		self.pll_alpha_sl = pll_alpha_sl
		self._pll_alpha_sl_slider.set_value(self.pll_alpha_sl)
		self._pll_alpha_sl_text_box.set_value(self.pll_alpha_sl)
		self.gr_costas_loop_cc_0.set_alpha(self.pll_alpha_sl)
		self.gr_costas_loop_cc_0.set_beta(self.pll_alpha_sl*self.pll_alpha_sl/4.0)

	def set_gain_tb(self, gain_tb):
		self.gain_tb = gain_tb
		self._gain_tb_text_box.set_value(self.gain_tb)

	def set_freq_tb(self, freq_tb):
		self.freq_tb = freq_tb
		self._freq_tb_text_box.set_value(self.freq_tb)

	def set_frames_file_text_inf(self, frames_file_text_inf):
		self.frames_file_text_inf = frames_file_text_inf
		self._frames_file_text_inf_static_text.set_value(self.frames_file_text_inf)

	def set_deframer_sync_after_text(self, deframer_sync_after_text):
		self.deframer_sync_after_text = deframer_sync_after_text
		self._deframer_sync_after_text_static_text.set_value(self.deframer_sync_after_text)

	def set_deframer_nosync_after_text(self, deframer_nosync_after_text):
		self.deframer_nosync_after_text = deframer_nosync_after_text
		self._deframer_nosync_after_text_static_text.set_value(self.deframer_nosync_after_text)

	def set_deframer_check_sync_text(self, deframer_check_sync_text):
		self.deframer_check_sync_text = deframer_check_sync_text
		self._deframer_check_sync_text_static_text.set_value(self.deframer_check_sync_text)

	def set_datetime_text(self, datetime_text):
		self.datetime_text = datetime_text
		self._datetime_text_static_text.set_value(self.datetime_text)

	def set_clock_alpha_sl(self, clock_alpha_sl):
		self.clock_alpha_sl = clock_alpha_sl
		self._clock_alpha_sl_slider.set_value(self.clock_alpha_sl)
		self._clock_alpha_sl_text_box.set_value(self.clock_alpha_sl)
		self.gr_clock_recovery_mm_xx_0.set_gain_omega(self.clock_alpha_sl*self.clock_alpha_sl/4.0)
		self.gr_clock_recovery_mm_xx_0.set_gain_mu(self.clock_alpha_sl)

	def set_baseband_file_text_inf(self, baseband_file_text_inf):
		self.baseband_file_text_inf = baseband_file_text_inf
		self._baseband_file_text_inf_static_text.set_value(self.baseband_file_text_inf)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--deframer-insync-frames", dest="deframer_insync_frames", type="intx", default=2,
		help="Set Count of valid ASM's after which deframer go in to synced state [default=%default]")
	parser.add_option("", "--viterbi-insync-frames", dest="viterbi_insync_frames", type="intx", default=5,
		help="Set Count of valid data BER test's after which Viterbi go in to synced state [default=%default]")
	parser.add_option("", "--deframer-outsync-frames", dest="deframer_outsync_frames", type="intx", default=5,
		help="Set Count of invalid ASM's after which deframer go out of synced state [default=%default]")
	parser.add_option("", "--viterbi-outsync-frames", dest="viterbi_outsync_frames", type="intx", default=20,
		help="Set Count of  non valid data BER test's after which Viterbi go out of synced state [default=%default]")
	parser.add_option("", "--viterbi-sync-threshold", dest="viterbi_sync_threshold", type="eng_float", default=eng_notation.num_to_str(0.1),
		help="Set Viterbi node sync threshold [BER] [default=%default]")
	parser.add_option("", "--clock-alpha", dest="clock_alpha", type="eng_float", default=eng_notation.num_to_str(0.005),
		help="Set Clock alpha [default=%default]")
	parser.add_option("", "--symb-rate", dest="symb_rate", type="intx", default=293883,
		help="Set Symbol rate [default=%default]")
	parser.add_option("", "--pll-alpha", dest="pll_alpha", type="eng_float", default=eng_notation.num_to_str(0.005),
		help="Set PLL alpha [default=%default]")
	parser.add_option("", "--satellite", dest="satellite", type="string", default='GOES-LRIT',
		help="Set Satellite [default=%default]")
	parser.add_option("", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(1691.02e6),
		help="Set Frequency [default=%default]")
	parser.add_option("", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(23),
		help="Set Gain [default=%default]")
	parser.add_option("", "--decim", dest="decim", type="intx", default=108,
		help="Set Decimation [default=%default]")
	parser.add_option("", "--side", dest="side", type="string", default="A",
		help="Set Side [default=%default]")
	parser.add_option("", "--frames-file", dest="frames_file", type="string", default=os.environ['HOME'] + '/GOES-LRIT_cadu_frames.cadu',
		help="Set CADU frames output filename [default=%default]")
	parser.add_option("", "--baseband-file", dest="baseband_file", type="string", default=os.environ['HOME'] + '/GOES-LRIT_baseband.dat',
		help="Set Baseband output filename [default=%default]")
	(options, args) = parser.parse_args()
	tb = file_rx_goes_lrit_fr(deframer_insync_frames=options.deframer_insync_frames, viterbi_insync_frames=options.viterbi_insync_frames, deframer_outsync_frames=options.deframer_outsync_frames, viterbi_outsync_frames=options.viterbi_outsync_frames, viterbi_sync_threshold=options.viterbi_sync_threshold, clock_alpha=options.clock_alpha, symb_rate=options.symb_rate, pll_alpha=options.pll_alpha, satellite=options.satellite, freq=options.freq, gain=options.gain, decim=options.decim, side=options.side, frames_file=options.frames_file, baseband_file=options.baseband_file)
	tb.Run(True)

