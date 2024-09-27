# Test Case Generation Documentation

This document provides an overview of the keyword parameters required for generating test cases using the `write_single_case` function. Each section describes different parameters and their expected outputs.

## Keyword Parameters

1. **gate_freq**: The frequency of the gate.
2. **mode**: The mode of dimension generation. Can be "uniform", "normal_lo", or "normal_hi".
3. **br_prob**: The probability of breaking out of the wire generation loop.
4. **dim_lo**: The lower bound for the dimensions.
5. **dim_hi**: The upper bound for the dimensions.
6. **pin_density**: The density of the pins, based on how many pins we want per gate and MAX_PINS.
7. **max_pin_freq**: The maximum frequency of the pins.
8. **override_specs**: Whether to override the specifications for manual checking of test cases.

## Example Test Cases -

### Test Case 1

kw = 
## Notes
- Ensure that the file paths specified in the `FP_SINGLE_IN` and `FP_SINGLE_OUT` constants are correct and accessible.
- Modify the parameters as needed to generate different test cases for various scenarios.