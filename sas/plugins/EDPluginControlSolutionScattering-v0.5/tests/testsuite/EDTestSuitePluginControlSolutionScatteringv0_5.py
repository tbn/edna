#coding: utf8
#
#    Project: Solution Scattering
#             http://www.edna-site.org
#
#    File: "$Id$"
#
#    Copyright (C) 2011 DLS
#                  2012 ESRF
#
#    Principal author:       irakli
#                            Jérôme Kieffer (jerome.kieffer@esrf.fr)
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

__authors__ = ["irakli", "Jérôme Kieffer"]
__license__ = "GPLv3+"
__copyright__ = "2011 DLS; 2012 ESRF"
__date__ = "20120214"

from EDTestSuite  import EDTestSuite

class EDTestSuitePluginControlSolutionScatteringv0_5(EDTestSuite):
    """
    This is the test suite for EDNA plugin SolutionScatteringv0_5 
    It will run subsequently all unit tests and execution tests.     
    """

    def process(self):
        #self.addTestCaseFromName("EDTestCasePluginUnitControlSolutionScatteringv0_3")
        self.addTestCaseFromName("EDTestCasePluginExecuteControlSolutionScatteringv0_5")



if __name__ == '__main__':

    edTestSuite = EDTestSuitePluginControlSolutionScatteringv0_5("EDTestSuitePluginControlSolutionScatteringv0_5")
    edTestSuite.execute()

