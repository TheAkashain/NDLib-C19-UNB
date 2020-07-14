"""
The :mod:`ndlib.models.epidemic` module contains common network models from epidemic research literature.
"""

from .GeneralisedThresholdModel import GeneralisedThresholdModel
from .IndependentCascadesModel import IndependentCascadesModel
from .KerteszThresholdModel import KerteszThresholdModel
from .ProfileModel import ProfileModel
from .ProfileThresholdModel import ProfileThresholdModel
from .SEIRModel import SEIRModel
from .SEISModel import SEISModel
from .SIModel import SIModel
from .SIRModel import SIRModel
from .SISModel import SISModel
from .SWIRModel import SWIRModel
from .ThresholdModel import ThresholdModel
from .ICEModel import ICEModel
from .ICPModel import ICPModel
from .GeneralThresholdModel import GeneralThresholdModel
from .UTLDRModel import UTLDRModel
from .SLLAIAIR import SLLAIAIR
from .Patient0Model import Patient0Model
from .ASPhaseModel import ASPhaseModel

__all__ = [
    'ASPhaseModel',
    'GeneralisedThresholdModel',
    'IndependentCascadesModel',
    'KerteszThresholdModel',
    'Patient0Model',
    'ProfileModel',
    'ProfileThresholdModel',
    'SEIRModel',
    'SEISModel',
    'SIModel',
    'SIRModel',
    'SISModel',
    'SLLAIAIR',
    'SWIRModel',
    'ThresholdModel',
    'ICEModel',
    'ICPModel',
    'GeneralThresholdModel',
    'UTLDRModel'
]
