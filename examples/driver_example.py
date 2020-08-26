"""Example using resources and drivers."""

import comet
from comet import ui

app = comet.Application("comet-example")

# Register resources
app.resources.add("INSTR", comet.Resource("ASRL2::INSTR", visa_library="@sim"))

# Load stored settings (optional)
app.resources.load_settings()

def on_click():
    """Read IDN from IEC60488 compatible resource."""
    try:
        with app.resources.get("INSTR") as instr:
            idn_text.value = comet.IEC60488(instr).identification
    except comet.ResourceError as exc:
        ui.show_exception(exc)

idn_text = ui.Text(readonly=True)

app.layout = ui.Column(
    ui.Row(
        idn_text,
        ui.Button("Reload", clicked=on_click)
    ),
    ui.Spacer(),
    stretch=(0, 1)
)

app.run()
