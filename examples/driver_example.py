"""Example using resources and drivers."""

import comet

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
        comet.show_exception(exc)

idn_text = comet.Text(readonly=True)

app.layout = comet.Column(
    comet.Row(
        idn_text,
        comet.Button("Reload", clicked=on_click)
    ),
    comet.Spacer(),
    stretch=(0, 1)
)

app.run()
