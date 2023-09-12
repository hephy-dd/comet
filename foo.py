from comet.parameter import ParameterBase, Parameter

class Measurement(ParameterBase):

    voltage_level = Parameter(unit="V", minimum=-1000, maximum=1000)
    current_compliance = Parameter(default="25 uA", unit="A", minimum=0, maximum="10 mA")
    write_output = Parameter(default=True, type=bool)

measurement = Measurement({"voltage_level": "100 V"})  # supply required parameters
print("### 1 #")

# Get dictionary of all parameter values.
measurement.parameters
# {'voltage_level': 100.0, 'current_compliance': 2.5e-05, 'write_output': True}
print(measurement.parameters)

# Update parameter values
print(measurement.update_parameters({"current_compliance": "10 mA"}))

# Access individual parameter
print(measurement.voltage_level)
# 100.0
print(measurement.current_compliance)
# 5e-05
print(measurement.write_output)
# True

# measurement.write_output = False
# AttributeError: can't set parameter: 'write_output'
print("###############")
from comet.utils import ureg, to_unit

value = ureg("25 nA")

print(to_unit(value, "mA"))
# 2.5e-05

print(to_unit(value, "nA"))
# 25

print(to_unit("1200 V", "kV"))
# 1.2

print(to_unit(2.5, "pA"))
# 2.5e-05
