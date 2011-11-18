#
#    Project: mxPluginExec
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) 2011      European Synchrotron Radiation Facility
#                            Grenoble, France
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    and the GNU Lesser General Public License  along with this program.  
#    If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "Thomas Boeglin"
__contact__ = "thomas.boeglin@esrf.fr"
__license__ = "LGPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"

import os, datetime

from EDPluginExec import EDPluginExec
from EDFactoryPluginStatic import EDFactoryPluginStatic

EDFactoryPluginStatic.loadModule("EDInstallSudsv0_4")
from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds.sax.date import DateTime

from XSDataCommon import XSDataInteger
from XSDataCommon import XSDataFile

from XSDataISPyBv1_3 import XSDataInputStoreDataCollection
from XSDataISPyBv1_3 import XSDataResultStoreDataCollection

class EDPluginISPyBRetrieveDataCollectionv1_3(EDPluginExec):
    """
    Plugin to retrieve results in an ISPyB database using web services
    """

    def __init__(self):
        """
        Sets default values for dbserver parameters 
        """
        EDPluginExec.__init__(self)
        self.setXSDataInputClass(XSDataFile)
        self.strUserName = None
        self.strPassWord = None
        self.strToolsForMXCubeWebServiceWsdl = None
        self.bContinue = True

    def configure(self):
        """
        Gets the web servise wdsl parameters from the config file and stores them in class member attributes.
        """
        EDPluginExec.configure(self)
        self.strUserName = self.getStringConfigurationParameterValue("userName")
        if self.strUserName is None:
            self.ERROR("EDPluginISPyBRetrieveDataCollectionv1_3.configure: No user name found in configuration!")
            self.setFailure()
        self.strPassWord = self.getStringConfigurationParameterValue("passWord")
        if self.strPassWord is None:
            self.ERROR("EDPluginISPyBRetrieveDataCollectionv1_3.configure: No pass word found in configuration!")
            self.setFailure()
        self.strToolsForMXCubeWebServiceWsdl = self.getStringConfigurationParameterValue("toolsForMXCubeWebServiceWsdl")
        if self.strToolsForMXCubeWebServiceWsdl is None:
            self.ERROR("EDPluginISPyBRetrieveDataCollectionv1_3.configure: No toolsForMXCubeWebServiceWsdl found in configuration!")
            self.setFailure()


    def process(self, _edObject=None):
        """
        Retrieves the contents of the DataCollectionContainer in ISPyB
        """
        EDPluginExec.process(self)
        self.DEBUG("EDPluginISPyBRetrieveDataCollectionv1_3.process")
        infile = self.getDataInput()
        inpath = infile.getPath()
        indir = os.path.dirname(inpath)
        infilename = os.path.basename(inpath)
        httpAuthenticatedToolsForMXCubeWebService = HttpAuthenticated(username=self.strUserName, password=self.strPassWord)
        clientToolsForMXCubeWebService = Client(self.strToolsForMXCubeWebServiceWsdl, transport=httpAuthenticatedToolsForMXCubeWebService)

        # DataCollectionProgram
        self.collectParameters = clientToolsForMXCubeWebService.findDataCollectionFromFileLocationAndFileName(indir, infilename)
        if self.collectParameters is None:
            self.ERROR("Couldn't find collect for file %s in ISPyB!" % inpath)
            self.setFailure()
            self.bContinue = False


    def postProcess(self, _edObject=None):
        """
        """
        EDPluginExec.postProcess(self)
        self.DEBUG("EDPluginISPyBRetrieveDataCollectionv1_3.postProcess")
        self.setDataOutput(self.collectParameters)


    def getValue(self, _oValue, _oDefaultValue=None):
        if _oValue is None:
            oReturnValue = _oDefaultValue
        else:
            oReturnValue = _oValue
        return oReturnValue


    def getDateValue(self, _strValue, _strFormat, _oDefaultValue):
        if _strValue is None:
            oReturnValue = _oDefaultValue
        else:
            try:
                oReturnValue = DateTime(datetime.datetime.strptime(_strValue, _strFormat))
            except:
                oReturnValue = DateTime(datetime.datetime.strptime(_strValue, _strFormat))
        return oReturnValue

