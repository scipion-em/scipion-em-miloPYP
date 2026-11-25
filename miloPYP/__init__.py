# **************************************************************************
# *
# * Authors:     you (you@yourinstitution.email)
# *
# * your institution
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
import pyworkflow.utils as pwutils
import pwem
from pyworkflow import TOMO

from miloPYP.constants import *

__version__ = '3.0.0'
_logo = "icon.png"
_references = ['Huang2024']


class Plugin(pwem.Plugin):
    _supportedVersions = [V3_2_8]
    _url = "https://github.com/scipion-em/scipion-em-miloPYP"
    _processingField = [TOMO]

    @classmethod
    def _defineVariables(cls):
        cls._defineVar(MILOPYP_ENV_ACTIVATION, MILOPYP_DEFAULT_ENV_ACTIVATION)
        cls._defineEmVar(MILOPYP_HOME, MILOPYP + '-' + MILOPYP_DEFAULT_VERSION)

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch my program. """
        environ = pwutils.Environ(os.environ)

        # ...

        return environ

    @classmethod
    def getDependencies(cls):
        """ Return a list of dependencies. """
        # try to get CONDA activation command
        condaActivationCmd = cls.getCondaActivationCmd()
        neededProgs = []
        if not condaActivationCmd:
            neededProgs.append('conda')
        return neededProgs

    @classmethod
    def defineBinaries(cls, env):
        MILOPYP_INSTALLED =f'{MILOPYP_ENV_NAME}_{MILOPYP_DEFAULT_VERSION}_installed'
        installationCmd = cls.getCondaActivationCmd()

        # Create the environment
        installationCmd += (f'conda create --name {MILOPYP_ENV_NAME} python={PYTHON_VERSION} &&')

        # Activate the env
        installationCmd += f'conda activate {MILOPYP_ENV_NAME} &&'

        # Clone the cet-pick repo
        installationCmd += 'git clone https://github.com/nextpyp/cet_pick.git &&'




        # checkpoint
        MILOPYP_commands = [(installationCmd,MILOPYP_INSTALLED)]

        env.addPackage(MILOPYP, version=MILOPYP_DEFAULT_VERSION,
                       tar='void.tgz',
                       commands=MILOPYP_commands,
                       neededProgs=cls.getDependencies(),
                       default=True)
