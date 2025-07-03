from opendbc.car import get_safety_config, structs
from opendbc.car.interfaces import CarInterfaceBase
from opendbc.car.rivian.carcontroller import CarController
from opendbc.car.rivian.carstate import CarState
from opendbc.car.rivian.radar_interface import RadarInterface
from opendbc.car.rivian.values import CAR, RivianSafetyFlags


class CarInterface(CarInterfaceBase):
  CarState = CarState
  CarController = CarController
  RadarInterface = RadarInterface

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, alpha_long, is_release, docs) -> structs.CarParams:
    ret.brand = "rivian"

    ret.safetyConfigs = [get_safety_config(structs.CarParams.SafetyModel.rivian)]

    # Generation-specific tuning
    if candidate in (CAR.RIVIAN_R1_GEN2,):
      # Gen2 improvements
      ret.steerActuatorDelay = 0.12  # Reduced delay for better responsiveness
      ret.steerLimitTimer = 0.35     # Faster recovery from steering limits
      ret.longitudinalActuatorDelay = 0.25  # Improved longitudinal response
      
      # Enhanced lateral tuning for Gen2
      CarInterfaceBase.configure_torque_tune(candidate, ret.lateralTuning)
      # Additional Gen2-specific lateral tuning
      ret.lateralTuning.torque.friction = 0.12  # Improved friction model
      
      # Gen2 longitudinal improvements - proof of concept
      ret.alphaLongitudinalAvailable = True
      if alpha_long:
        ret.openpilotLongitudinalControl = True
        ret.safetyConfigs[0].safetyParam |= RivianSafetyFlags.LONG_CONTROL.value
        # Gen2 enhanced longitudinal parameters
        ret.longitudinalActuatorDelay = 0.25
        ret.vEgoStopping = 0.2  # Better stop control
        ret.stopAccel = -0.3   # Improved stopping
    else:
      # Gen1 parameters (existing)
      ret.steerActuatorDelay = 0.15
      ret.steerLimitTimer = 0.4
      CarInterfaceBase.configure_torque_tune(candidate, ret.lateralTuning)
      
      # Gen1 longitudinal (existing behavior)
      ret.alphaLongitudinalAvailable = False
      if alpha_long:
        ret.openpilotLongitudinalControl = True
        ret.safetyConfigs[0].safetyParam |= RivianSafetyFlags.LONG_CONTROL.value
      
      ret.longitudinalActuatorDelay = 0.35
      ret.vEgoStopping = 0.25
      ret.stopAccel = 0

    ret.steerControlType = structs.CarParams.SteerControlType.torque
    ret.radarUnavailable = True

    return ret
