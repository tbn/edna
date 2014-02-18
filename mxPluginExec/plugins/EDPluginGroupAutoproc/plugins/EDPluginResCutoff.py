from __future__ import with_statement

# coding: utf8
#
#    Project: <projectName>
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) <copyright>
#
#    Principal author:       <author>
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



__author__="thomas boeglin"
__license__ = "GPLv3+"
__copyright__ = "<copyright>"




import os.path
import shutil

from EDPlugin import EDPlugin
from EDVerbose import EDVerbose
from XSDataCommon import XSDataBoolean, XSDataFloat, XSDataVectorDouble
from XSDataAutoproc import XSDataResCutoff, XSDataResCutoffResult
from XSDataAutoproc import XSData2DCoordinates, XSDataXdsCompletenessEntry


class EDPluginResCutoff(EDPlugin):
    """
    """


    def __init__(self ):
        """
        """
        EDPlugin.__init__(self )
        self.setXSDataInputClass(XSDataResCutoff)

    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginParseXdsOutput.checkParameters")

        data_input = self.dataInput
        self.checkMandatoryParameters(data_input.completeness_entries,
                                      "no completeness entries in input")

    def preProcess(self, _edObject = None):
        EDPlugin.preProcess(self)
        self.DEBUG("EDPluginParseXdsOutput.preProcess")

    def process(self, _edObject = None):
        EDPlugin.process(self)

        cchalf_cutoff = 30
        cchalf_cutoff_param = self.dataInput.cc_half_cutoff
        if cchalf_cutoff_param is not None:
            cchalf_cutoff = cchalf_cutoff_param.value

        bins = list()

        for entry in self.dataInput.completeness_entries:
            res = entry.res.value
            cchalf = entry.half_dataset_correlation.value
            bins.append(res)
            if cchalf < cchalf_cutoff:
                break

        if len(bins) < 2:
            EDVerbose.DEBUG("No bins with CC1/2 greater than %s" % cchalf_cutoff)
            EDVerbose.DEBUG("""something could be wrong, or the completeness could be too low!
bravais lattice/SG could be incorrect or something more insidious like
incorrect parameters in XDS.INP like distance, X beam, Y beam, etc.
Stopping""")
            self.setFailure()
            return

        retbins = [XSDataFloat(x) for x in bins]
        final_res = bins[-1]


        data_output = XSDataResCutoffResult()
        data_output.res = XSDataFloat(final_res)
        data_output.bins = retbins
        totals = self.dataInput.total_completeness
        data_output.total_complete = totals.complete
        data_output.total_rfactor = totals.rfactor
        data_output.total_isig = totals.isig

        self.dataOutput = data_output

    def postProcess(self, _edObject = None):
        EDPlugin.postProcess(self)
        self.DEBUG("EDPluginParseXdsOutput.postProcess")
