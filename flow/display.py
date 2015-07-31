
from flow import Block, Signal, Input

from pyqtgraph import QtGui, PlotWidget

from traits.api import Bool, List, on_trait_change

class Oscilloscope(Block):

	autoscale = Bool(True)
	channels = List(Input())

	def __init__(self, name, **config):
		self._plot_widget = PlotWidget(title=name)
		self._plot_widget.block = self

		self.plots = {}

		super(Oscilloscope, self).__init__(**config)


	@on_trait_change('channels[]')
	def channels_changed(self, object, name, old, new):
		for channel in old:
			del self.plots[channel]
		for channel in new:
			plot = self._plot_widget.plot()
			
			if isinstance(channel.color, QtGui.QColor):
				color = channel.color
			else:
				color = QtGui.qRgb(*channel.color)
			
			plot.setPen(QtGui.QColor(color))
			self.plots[channel] = plot

	def _autoscale_changed(self):
		self._plot_widget.enableAutoRange('y', self.autoscale)


	def widget(self):
		return self._plot_widget

	def updateGUI(self):
		for channel in self.plots:
			plot = self.plots[channel]
			plot.setData(channel.buffer)

	def process(self):
		pass

class Spectrograph(Block):
	def __init__(self, name, **config):
		super(Spectrograph, self).__init__(**config)

	def widget(self):
		return QtGui.QWidget()

class TextBox(Block):
	def __init__(self, name, **config):
		super(TextBox, self).__init__(**config)
