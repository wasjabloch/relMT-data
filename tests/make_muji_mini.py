#! /usr/bin/env python

"""
Make the minimal relMT dataset from example1 provided with the main code
"""
import numpy as np
from relmt import io, core

# Output directory
dir = "muji-mini/"

# Events and stations to include
evns = [7640, 7508, 8459, 7642, 5964, 11424]
stas = ["P116", "CHE6", "EP03", "EP11", "EP10"]

# Full station and event tables
evd = io.read_event_table("muji/data/events.txt")
std = io.read_station_table("muji/data/stations.txt")
phd = io.read_phase_table("muji/data/phases.txt")
mtd = io.read_mt_table("muji/data/reference_mts.txt")

# Reduces station and event tables
evd2 = {evn: ev for evn, ev in evd.items() if evn in evns}
std2 = {code: station for code, station in std.items() if code in stas}
phd2 = {phid: phase for phid, phase in phd.items() if core.split_phaseid(phid)[0] in evns and core.split_phaseid(phid)[1] in stas}
io.write_station_table(std2, dir + "/data/stations.txt")
io.write_event_table(evd2, dir + "/data/events.txt")
io.write_mt_table(mtd, dir + "/data/reference_mts.txt")
io.write_phase_table(phd2, dir + "/data/phases.txt")

for wvid in core.iterate_waveid(stas):
    sta, pha = core.split_waveid(wvid)
    arr, hdr = io.read_waveform_array_header(sta, pha, 0, "muji")
    ievs = [hdr["events_"].index(evn) for evn in evns]
    arr2 = arr[ievs, :, :]
    hdr["events_"] = evns
    hdrf = core.file("waveform_header", sta, pha, 0, dir)
    arrf = core.file("waveform_array", sta, pha, 0, dir)
    hdr.to_file(hdrf, True)
    np.save(arrf, arr)
