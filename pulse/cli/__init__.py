"""CLI interface module"""

import click
import pulsectl

from pulse.notification import send_notification

CLIENT="pulse"
INCREMENT = 0.05
DECREMENT = -0.05

@click.command
def vup():
    with pulsectl.Pulse(CLIENT) as pulse:
        current_sink: pulsectl.PulseSinkInfo = pulse.get_sink_by_name(
            pulse.server_info().default_sink_name
        )
        pulse.volume_change_all_chans(current_sink, INCREMENT)


@click.command
def vdown():
    with pulsectl.Pulse(CLIENT) as pulse:
        current_sink: pulsectl.PulseSinkInfo = pulse.get_sink_by_name(
            pulse.server_info().default_sink_name
        )
        pulse.volume_change_all_chans(current_sink, DECREMENT)


@click.command
def tmute():
    """Toggles the current PulseAudio sink to mute/unmute."""
    with pulsectl.Pulse(CLIENT) as pulse:
        current_sink: pulsectl.PulseSinkInfo = pulse.get_sink_by_name(
            pulse.server_info().default_sink_name
        )
        mute = current_sink.mute
        pulse.mute(current_sink, not mute)


@click.command
def next_sink():
    """Switches to the next PulseAudio sink interface."""
    with pulsectl.Pulse(CLIENT) as pulse:
        sinks: list[pulsectl.PulseSinkInfo] = pulse.sink_list()

        if not sinks or len(sinks) == 1:
            return

        current_sink: pulsectl.PulseSinkInfo = pulse.get_sink_by_name(
            pulse.server_info().default_sink_name
        )

        sorted_sinks = sorted(sinks, key=lambda sink: sink.index)
        sorted_index = [sink.index for sink in sorted_sinks]

        current_position = sorted_index.index(current_sink.index)

        next_position = 0
        if current_position < len(sorted_index) - 1:
            next_position = current_position + 1

        next_sink = sorted_sinks[next_position]
        pulse.sink_default_set(next_sink.name)
        sink_inputs = pulse.sink_input_list()
        for sink_input in sink_inputs:
            pulse.sink_input_move(sink_input.index, next_sink.index)

        send_notification(f"Audio Device: {next_sink.name} {next_sink.description}")


@click.group(commands=[vup, vdown, tmute, next_sink])
@click.version_option(None, "--version", package_name="pulse")
def cli() -> None:
    """CLI Runner group"""


if __name__ == "__main__":
    cli()
