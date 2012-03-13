# coding: utf8
#
#    Project: <projectName>
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) <copyright>
#
#    Principal author:        <author>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__author__="<author>"
__license__ = "GPLv3+"
__copyright__ = "<copyright>"


from EDPluginControl import EDPluginControl
from XSDataAutoProc import XSDataMinimalXdsIn
#from <xsDataBaseName> import <xsDataResultName>

class EDPluginControlRunXds( EDPluginControl ):
    """
    Runx XDS 3 times like Max's autoproc does.
    1. First run is a vanilla run
    2. Second run set JOB to DEFPIX INTEGRATE CORRECT
    3. Third run set JOB to ALL, maxproc to 4 and maxjobs to 1
    4. Final run set JOB to DEFPIX INTEGRATE CORRECT and maxproc and
    maxjobs like the 3rd run
    """


    def __init__( self ):
        """
        """
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataMinimalXdsIn)
        self.controlled_plugin_name = 'EDPluginMinimalXds'
        self.first_run = None
        self.second_run = None
        self.third_run = None
        self.final_run = None


    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginControlRunXds.checkParameters")
        self.checkMandatoryParameters(self.dataInput, "Data Input is None")
        self.checkMandatoryParameters(self.dataInput.input_file, "No XDS input file")


    def preProcess(self, _edObject = None):
        EDPluginControl.preProcess(self)
        self.DEBUG("EDPluginControl<pluginName>.preProcess")
        # Load the execution plugin
        self.first_run = self.loadPlugin(self.controlled_plugin_name)


    def process(self, _edObject = None):
        EDPluginControl.process(self)
        self.DEBUG("EDPluginControlRunXds.process")
        #self.__edPluginExecTemplate.connectSUCCESS(self.doSuccessExecTemplate)
        #self.__edPluginExecTemplate.connectFAILURE(self.doFailureExecTemplate)
        #self.__edPluginExecTemplate.executeSynchronous()

        # First run is vanilla without any modification
        params = XSDataMinimalXdsIn()
        params.input_file = self.dataInput.input_file

        self.first_run.dataInput = params
        self.firstRun.executeSynchronous()

        EDVerbose.DEBUG('first run completed...')

        if self.first_run.dataOutput is not None and self.first_run.dataOutput.succeeded:
            EDVerbose.DEBUG('... and it worked')
            return
        EDVerbose.DEBUG('... and it failed')


        # second run w/ JOB set to DEFPIX INTEGRATE CORRECT
        self.second_run = self.loadPlugin(self.controlled_plugin_name)
        params = XSDataMinimalXdsIn()
        params.input_file = self.dataInput.input_file
        params.jobs = 'DEFPIX INTEGRATE CORRECT'
        self.second_run.dataInput = params
        self.second_run.executeSynchronous()

        EDVerbose.DEBUG('second run completed')
        if self.second_run.dataOutput is not None and self.second_run.dataOutput.succeeded:
            EDVerbose.DEBUG('... and it worked')
            return
        EDVerbose.DEBUG('... and it failed')


        # third run with JOB set to ALL and mxaprocs = 4 and maxjobs = 1
        self.third_run = self.loadPlugin(self.controlled_plugin_name)
        params = XSDataMinimalXdsIn()
        params.input_file = self.dataInput.input_file
        params.jobs = 'ALL'
        params.maxprocs = 4
        params.maxjobs = 1
        self.third_run.dataInput = params
        self.third_run.executeSynchronous()

        EDVerbose.DEBUG('third run completed')
        if self.third_run.dataOutput is not None and self.third_run.dataOutput.succeeded:
            EDVerbose.DEBUG('... and it worked')
            return
        EDVerbose.DEBUG('... and it failed')


        # final run with parallelism like 3 but JOB like 2
        self.final_run = self.loadPlugin(self.controlled_plugin_name)
        params = XSDataMinimalXdsIn()
        params.input_file = self.dataInput.input_file
        params.jobs = 'DEFPIX INTEGRATE CORRECT'
        params.maxprocs = 4
        params.maxjobs = 1
        self.final_run.dataInput = params
        self.final_run.executeSynchronous()

        EDVerbose.DEBUG('final run completed')
        if self.final_run.dataOutput is not None and self.final_run.dataOutput.succeeded:
            EDVerbose.DEBUG('... and it worked')
            return
        EDVerbose.DEBUG('... and it failed')


    def postProcess(self, _edObject = None):
        EDPluginControl.postProcess(self)
        self.DEBUG("EDPluginControl<pluginName>.postProcess")
        # Create some output data
        xsDataResult = <xsDataResultName>()
        self.setDataOutput(xsDataResult)


    def doSuccessExecTemplate(self,  _edPlugin = None):
        self.DEBUG("EDPluginControl<pluginName>.doSuccessExecTemplate")
        self.retrieveSuccessMessages(_edPlugin, "EDPluginControl<pluginName>.doSuccessExecTemplate")


    def doFailureExecTemplate(self,  _edPlugin = None):
        self.DEBUG("EDPluginControl<pluginName>.doFailureExecTemplate")
        self.retrieveFailureMessages(_edPlugin, "EDPluginControl<pluginName>.doFailureExecTemplate")