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


import os
import os.path
import shutil
import fnmatch

from EDPluginExecProcessScript import EDPluginExecProcessScript
from EDVerbose import EDVerbose

from XSDataCommon import XSDataBoolean
from XSDataAutoproc import XSDataDimpleIn, XSDataDimpleOut
from xdscfgparser import parse_xds_file, dump_xds_file

# For reference:
#dimple [options...] input.mtz input.pdb output_dir
#
#optional arguments:
#  -h, --help            show this help message and exit
#  --hklout out.mtz      output mtz file (default: final.mtz)
#  --xyzout out.pdb      output pdb file (default: final.pdb)
#  -s, --summary         show refmac summary
#  -f {png,jpeg,tiff}    format of generated images (default: png)
#  --weight VALUE        refmac matrix weight (default: auto-weight)
#  -R MTZ_FILE, --free-r-flags MTZ_FILE
#                        reference file with all reflections and freeR flags
#  -I ICOL, --icolumn ICOL
#                        I column label (default: IMEAN)
#  --sigicolumn SIGICOL  SIGI column label (default: SIG<ICOL>)


class EDPluginExecDimple(EDPluginExecProcessScript):
    """Encapsulate a run of the dimple "script" that's part of the CCP4
    distribution

    """


    def __init__(self ):
        """
        """
        EDPluginExecProcessScript.__init__(self )
        self.setXSDataInputClass(XSDataDimpleIn)
        self.setRequireCCP4(True)


    def checkParameters(self):
        """
        Checks the mandatory parameters.
        """
        self.DEBUG("EDPluginExecDimple.checkParameters")
        self.checkMandatoryParameters(self.dataInput,"Data Input is None")
        self.checkMandatoryParameters(self.dataInput.input_pdb,"Input PDB not specified")
        self.checkMandatoryParameters(self.dataInput.input_mtz,"Input MTZ not specified")
        self.checkMandatoryParameters(self.dataInput.output_dir,"Output directory not specified")



    def preProcess(self, _edObject = None):
        EDPluginExecProcessScript.preProcess(self)
        self.DEBUG("EDPluginMinimalXDS.preProcess")

        # First let's check if the input files really exist
        inpdb = self.dataInput.input_pdb.value
        inmtz = self.dataInput.input_mtz.value
        outdir = self.dataInput.output_dir.value

        for f in (inpdb, inmtz):
            if not os.path.isfile(f):
                EDVerbose.ERROR('the following input file does not exist: {0}'.format(f))
                raise ValueError('Invalid input file {0}'.format(f))
        if not os.path.isdir(outdir):
            EDVerbose.ERROR('the output directory does not exist: {0}'.format(outdir))
            raise ValueError('Invalid output directory {0}'.format(outdir))


        self.basic_options = "{0} {1} {2}".format(self.dataInput.input_mtz.value,
                                                  self.dataInput.input_pdb.value,
                                                  self.dataInput.output_dir.value)
        # Now the other optional ones
        additional_opts = []
        if self.dataInput.icol:
            additional_opts.append('--icolumn {0}'.format(self.dataInput.icol.value))
        if self.dataInput.sigi_col:
            additional_opts.append('--sigicolumn {0}'.format(self.dataInput.sigi_col.value))
        if self.dataInput.output_mtz:
            additional_opts.append('--hklout {0}'.format(self.dataInput.output_mtz.value))
        if self.dataInput.output_pdb:
            additional_opts.append('--xyzout {0}'.format(self.dataInput.output_pdb.value))


        cmdline = '{0} {1}'.format(' '.join(additional_opts),
                                          self.basic_options)
        self.setScripCommandLine(cmdline)
        self.DEBUG('set the command line options to {0}'.format(cmdline))

    def process(self, _edObject = None):
        EDPluginExecProcessScript.process(self)
        self.DEBUG("EDPluginDimple.process")


    def postProcess(self, _edObject = None):
        EDPluginExecProcessScript.postProcess(self)
        self.DEBUG("EDPluginDimple.postProcess")
