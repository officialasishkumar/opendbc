from opendbc.car.rivian.fingerprints import FW_VERSIONS
from opendbc.car.rivian.values import CAR, FW_QUERY_CONFIG, WMI, ModelLine, ModelYear


class TestRivian:
  def test_custom_fuzzy_fingerprinting(self, subtests):
    for platform in CAR:
      with subtests.test(platform=platform.name):
        for wmi in WMI:
          for line in ModelLine:
            for year in ModelYear:
              for bad in (True, False):
                vin = ["0"] * 17
                vin[:3] = wmi
                vin[3] = line.value
                vin[9] = year.value
                if bad:
                  vin[3] = "Z"
                vin = "".join(vin)

                matches = FW_QUERY_CONFIG.match_fw_to_car_fuzzy({}, vin, FW_VERSIONS)
                
                # Updated logic for Gen2 support
                if platform == CAR.RIVIAN_R1_GEN1:
                  should_match = year in (ModelYear.N_2022, ModelYear.P_2023, ModelYear.R_2024) and not bad
                elif platform == CAR.RIVIAN_R1_GEN2:
                  should_match = year in (ModelYear.S_2025, ModelYear.T_2026) and not bad
                else:
                  should_match = False
                
                expected = {str(platform)} if should_match else set()
                assert matches == expected, f"Bad match for {platform.name}, year {year}, vin {vin}"

  def test_gen2_longitudinal_support(self):
    """Test that Gen2 models have enhanced longitudinal support"""
    gen2_platform = CAR.RIVIAN_R1_GEN2
    
    # Verify Gen2 is in the platform list
    assert gen2_platform in CAR
    
    # Verify Gen2 has proper model years
    assert ModelYear.S_2025 in gen2_platform.config.years
    assert ModelYear.T_2026 in gen2_platform.config.years
    
    # Verify Gen2 supports both R1T and R1S
    assert ModelLine.R1T in gen2_platform.config.lines
    assert ModelLine.R1S in gen2_platform.config.lines

  def test_gen2_enhanced_specs(self):
    """Test that Gen2 has improved specifications"""
    gen1 = CAR.RIVIAN_R1_GEN1
    gen2 = CAR.RIVIAN_R1_GEN2
    
    # Gen2 should have improved steer ratio for better lateral control
    assert gen2.config.specs.steerRatio < gen1.config.specs.steerRatio
    
    # Gen2 should have reduced mass for better efficiency
    assert gen2.config.specs.mass < gen1.config.specs.mass
