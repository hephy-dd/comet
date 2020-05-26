"""Example registering and listing resources.

Use Edit -> Preferences... to edit the resources and see changes after
application restart.
"""

import comet

app = comet.Application("comet-example")

# Register resources
app.resources.add("SMU", comet.Resource("ASRL1::INSTR", visa_library="@sim"))
app.resources.add("ELM", comet.Resource("ASRL2::INSTR", visa_library="@sim"))
app.resources.add("LCR", comet.Resource("ASRL3::INSTR", visa_library="@sim"))

# Load stored settings (optional)
app.resources.load_settings()

table = comet.Table(header=["Name", "Resource", "VISA Library"])

# List resources
for name, resource in app.resources.items():
    table.append([name, resource.resource_name, resource.visa_library])

table.fit()
app.layout = table

app.run()
