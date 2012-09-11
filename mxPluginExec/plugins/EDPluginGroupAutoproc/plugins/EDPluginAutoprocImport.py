from __future__ import with_statement

# coding: utf8
#
#    Project: Autoproc
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) ESRF
#
#    Principal author: Thomas Boeglin
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

__author__="Thomas Boeglin"
__license__ = "GPLv3+"
__copyright__ = "ESRF"

import re
import os.path
import tempfile

from EDPluginControl import EDPluginControl

from XSDataCommon import XSDataStatus, XSDataBoolean, XSDataResult, XSDataString
from XSDataAutoproc import XSDataAutoprocImport, XSDataAutoprocImportOut
from XSDataAutoproc import XSDataFileConversion

OUTFILE_TEMPLATE = 'unmerged_{0}.mtz'

class EDPluginAutoprocImport(EDPluginControl):
    def __init__(self):
        EDPluginControl.__init__(self)
        self.setXSDataInputClass(XSDataAutoprocImport)

    def configure(self):
        EDPluginControl.configure(self)

    def preProcess(self):
        EDPluginControl.preProcess(self)
        self.DEBUG('Import : preprocess')
        self.anom_anom = self.loadPlugin('EDPluginControlFileConversion')
        self.anom_noanom = self.loadPlugin('EDPluginControlFileConversion')
        self.noanom_anom = self.loadPlugin('EDPluginControlFileConversion')
        self.noanom_noanom = self.loadPlugin('EDPluginControlFileConversion')
        tocopy = ['dataCollectionID', 'start_image', 'end_image', 'res', 'nres']

        anom_anom_in = XSDataFileConversion()
        anom_noanom_in = XSDataFileConversion()
        noanom_anom_in = XSDataFileConversion()
        noanom_noanom_in = XSDataFileConversion()

        # copy the common attributes from our data model to the subplugins'
        for a in tocopy:
            for dm in anom_anom_in, anom_noanom_in, noanom_anom_in, noanom_noanom_in:
                setattr(dm, a, getattr(self.dataInput, a))

        # now set the specific bits
        anom_anom_in.anom = XSDataBoolean(True)
        anom_anom_in.input_file = self.dataInput.input_anom_anom
        anom_anom_in.output_file = os.path.join(self.outdir, OUTFILE_TEMPLATE.format('anom_anom'))

        anom_noanom_in.anom = XSDataBoolean(False)
        anom_noanom_in.input_file = self.dataInput.input_anom_noanom
        anom_noanom_in.output_file = os.path.join(self.outdir, OUTFILE_TEMPLATE.format('anom_noanom'))

        noanom_anom_in.anom = XSDataBoolean(True)
        noanom_anom_in.input_file = self.dataInput.input_noanom_anom
        noanom_anom_in.output_file = os.path.join(self.outdir, OUTFILE_TEMPLATE.format('noanom_anom'))

        noanom_noanom_in.anom = XSDataBoolean(False)
        noanom_noanom_in.input_file = self.dataInput.input_noanom_noanom
        noanom_noanom_in.output_file = os.path.join(self.outdir, OUTFILE_TEMPLATE.format('noanom_noanom'))

    def checkParameters(self):
        # NB. we'll only check for the output directory existence for
        # now
        self.DEBUG('Import: checkParameters')
        outdir = self.dataInput.output_directory
        if outdir is None:
            self.ERROR('File Import: output directory not specified: aborting')
            self.setFailure()
            return

        self.outdir = outdir.value
        if not os.path.exists(outdir) and not os.path.isdir(outdir):
            self.ERROR('File Import: output directory is not a directory')
            self.setFailure()
            return


    def process(self):
        self.DEBUG('Import: process')
        EDPluginControl.process(self)

        # start all plugins
        for p in self.getListOfLoadedPlugin():
            p.execute()

        # wait for all the 4 plugins to finish
        self.synchronizePlugins()

    def postProcess(self):
        self.DEBUG('Import: postProcess')
        EDPluginControl.postProcess(self)

        res = XSDataAutoprocImportOut()
        status = XSDataStatus()
        res.status = status
        all_good = all([not x.isFailure() for x in self.getListOfLoadedPlugin()])
        status.isSuccess = XSDataBoolean(all_good)
        files = list()
        for p in self.getListOfLoadedPlugin():
            if not p.isFailure():
                files.append(p.dataInput.output_file)
        res.files = files

        self.dataOutput = res
