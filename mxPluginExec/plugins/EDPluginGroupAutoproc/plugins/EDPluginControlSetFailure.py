__author__="Thomas Boeglin"
__license__ = "GPLv3+"
__copyright__ = "ESRF"

from EDPluginControl import EDPluginControl
from EDVerbose import EDVerbose

from XSDataCommon import  XSDataInput

class EDPluginControlSetFailure(EDPluginControl):

    def __init__( self ):
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataInput)

    def checkParameters(self):
        self.DEBUG("EDPluginControlSetFailure.checkParameters")
        self.DEBUG('calling setFailure()')
        self.setFailure()

    def preProcess(self, _edObject = None):
        EDPluginControl.preProcess(self)
        self.DEBUG('EDPluginControlSetFailure.preProcess starting')
        self.DEBUG('self.isFailure() is {0}'.format(self.isFailure()))
        self.DEBUG('calling setFailure()')
        self.setFailure()

    def process(self, _edObject = None):
        EDPluginControl.process(self)
        self.DEBUG('EDPluginControlSetFailure.process starting')
        self.DEBUG('self.isFailure() is {0}'.format(self.isFailure()))
        self.DEBUG('calling setFailure()')
        self.setFailure()

    def postProcess(self, _edObject = None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginControlSetFailure.postProcess")
        self.DEBUG('self.isFailure() is {0}'.format(self.isFailure()))
        self.DEBUG('calling setFailure()')
        self.setFailure()
