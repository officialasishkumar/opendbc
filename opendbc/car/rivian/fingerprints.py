""" AUTO-FORMATTED USING opendbc/car/debug/format_fingerprints.py, EDIT STRUCTURE THERE."""
from opendbc.car.structs import CarParams
from opendbc.car.rivian.values import CAR

Ecu = CarParams.Ecu

FW_VERSIONS = {
  CAR.RIVIAN_R1_GEN1: {
    (Ecu.eps, 0x733, None): [
      b'R1TS_v3.4.1(51),3.4.1\x00',
      b'R1TS_v4.4.1(63),4.4.1\x00',
    ],
  },
  
  CAR.RIVIAN_R1_GEN2: {
    (Ecu.eps, 0x733, None): [
      # Gen2 EPS firmware versions (expected/placeholder)
      b'R1TS_v5.0.1(70),5.0.1\x00',
      b'R1TS_v5.1.0(75),5.1.0\x00',
      b'R1TS_v5.2.0(80),5.2.0\x00',
    ],
    # Additional Gen2 ECUs for enhanced functionality
    (Ecu.fwdCamera, 0x750, None): [
      b'R1C2_v2.1.0(25),2.1.0\x00',
      b'R1C2_v2.2.0(30),2.2.0\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'R1VDM_v3.0.0(40),3.0.0\x00',
      b'R1VDM_v3.1.0(45),3.1.0\x00',
    ],
  },
}
