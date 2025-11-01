#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json, re
import os
from asammdf import MDF, Signal



# --------------------------
#file_path = "20251101_174717500mvpwm.bin"

file_path = "20251101_16595210k.bin"

# {
#     "MODEL": "306400101",
#     "IDN": "OWON,XDS3064E,2009110,V2.3.1",
#     "channel": [
#         {
#             "Index": "CH1",
#             "Availability_Flag": "TRUE",
#             "Display_Switch": "OFF",
#             "Wave_Character": "CH1",
#             "Sample_Rate": "(2.5MS/s)",
#             "Acqu_Mode": "SAMPle",
#             "Storage_Depth": "10K",
#             "Display_Mode": "Normal",
#             "Hscale": "200us",
#             "Vscale": "50.0mV",
#             "Reference_Zero": "-148",
#             "Scroll_Pos_Time": "0.000000us",
#             "Trig_After_Time": "43996.000000us",
#             "Trig_Tops_Tme": "43996.000000us",
#             "Adc_Data_Time": "0.400000us",
#             "Adc_Data0_Time": "0.000000us",
#             "Voltage_Rate": "0.007813mv",
#             "Data_Length": "10000",
#             "Probe_Magnification": "10X",
#             "Current_Rate": 10000.0,
#             "Current_Ratio": 0.78125,
#             "Measure_Current_Switch": "OFF",
#             "Cyc": "999.904000us",
#             "Freq": "1000.096009Hz",
#             "PRECISION": 0
#         }
#     ]
# }
file_path = "20251101_174717500mvpwm.bin"

# === Full OWON Header ===
# {
#     "MODEL": "306400101",
#     "IDN": "OWON,XDS3064E,2009110,V2.3.1",
#     "channel": [
#         {
#             "Index": "CH1",
#             "Availability_Flag": "TRUE",
#             "Display_Switch": "OFF",
#             "Wave_Character": "CH1",
#             "Sample_Rate": "(2.5MS/s)",
#             "Acqu_Mode": "SAMPle",
#             "Storage_Depth": "10K",
#             "Display_Mode": "Normal",
#             "Hscale": "200us",
#             "Vscale": "50.0mV",
#             "Reference_Zero": "-148",
#             "Scroll_Pos_Time": "0.000000us",
#             "Trig_After_Time": "43996.000000us",
#             "Trig_Tops_Tme": "43996.000000us",
#             "Adc_Data_Time": "0.400000us",
#             "Adc_Data0_Time": "0.000000us",
#             "Voltage_Rate": "0.007813mv",
#             "Data_Length": "10000",
#             "Probe_Magnification": "10X",
#             "Current_Rate": 10000.0,
#             "Current_Ratio": 0.78125,
#             "Measure_Current_Switch": "OFF",
#             "Cyc": "999.904000us",
#             "Freq": "1000.096009Hz",
#             "PRECISION": 0
#         }
#     ]
# }
file_path = "20251101_2012483div.bin"

#out of range adc reading is 7f.
# {
#     "MODEL": "306400101",
#     "IDN": "OWON,XDS3064E,2009110,V2.3.1",
#     "channel": [
#         {
#             "Index": "CH1",
#             "Availability_Flag": "TRUE",
#             "Display_Switch": "OFF",
#             "Wave_Character": "CH1",
#             "Sample_Rate": "(2.5MS/s)",
#             "Acqu_Mode": "SAMPle",
#             "Storage_Depth": "10K",
#             "Display_Mode": "Normal",
#             "Hscale": "200us",
#             "Vscale": "5.00mV",
#             "Reference_Zero": "0", - means where I set the scope display cursor zero
#             "Scroll_Pos_Time": "0.000000us",
#             "Trig_After_Time": "43910.000000us",
#             "Trig_Tops_Tme": "43910.000000us",
#             "Adc_Data_Time": "0.400000us",
#             "Adc_Data0_Time": "0.000000us",
#             "Voltage_Rate": "0.000781mv",
#             "Data_Length": "10000",
#             "Probe_Magnification": "10X",
#             "Current_Rate": 10000.0,
#             "Current_Ratio": 0.078125,
#             "Measure_Current_Switch": "OFF",
#             "Cyc": "999.904000us",
#             "Freq": "1000.096009Hz",
#             "PRECISION": 0
#         }
#     ]
# }
#file_path = "20251101_194251zoom0.bin"
# === Full OWON Header ===
# {
#     "MODEL": "306400101",
#     "IDN": "OWON,XDS3064E,2009110,V2.3.1",
#     "channel": [
#         {
#             "Index": "CH1",
#             "Availability_Flag": "TRUE",
#             "Display_Switch": "OFF",
#             "Wave_Character": "CH1",
#             "Sample_Rate": "(2.5MS/s)",
#             "Acqu_Mode": "SAMPle",
#             "Storage_Depth": "10K",
#             "Display_Mode": "Normal",
#             "Hscale": "200us",
#             "Vscale": "2.00mV",
#             "Reference_Zero": "0",
#             "Scroll_Pos_Time": "0.000000us",
#             "Trig_After_Time": "43900.000000us",
#             "Trig_Tops_Tme": "43900.000000us",
#             "Adc_Data_Time": "0.400000us",
#             "Adc_Data0_Time": "0.000000us",
#             "Voltage_Rate": "0.000313mv",
#             "Data_Length": "10000",
#             "Probe_Magnification": "10X",
#             "Current_Rate": 10000.0,
#             "Current_Ratio": 0.03125,
#             "Measure_Current_Switch": "OFF",
#             "Cyc": "999.904000us",
#             "Freq": "1000.096009Hz",
#             "PRECISION": 0
#         }
#     ]
# }
# ========================================
#file_path = "20251101_195439railed.bin"

file_path = "20251031_193551fahrzeugdaten.bin"

# --------------------------

# --- Read file ---
with open(file_path, "rb") as f:
    blob = f.read()

# --- Find SPBXDS header ---
i = blob.find(b"SPBXDS")
if i < 0:
    raise ValueError("SPBXDS header not found")

# Find JSON bounds
j = blob.find(b"{", i)
depth, end = 0, None
for k in range(j, len(blob)):
    if blob[k] == 123: depth += 1
    elif blob[k] == 125: depth -= 1
    if depth == 0:
        end = k
        break
if end is None:
    raise ValueError("Could not find end of JSON header")

# --- Parse JSON header ---
txt = blob[j:end+1].decode("ascii","ignore")
txt = re.sub(r",\s*([}\]])", r"\1", txt)  # remove trailing commas
header = json.loads(txt)

# --- Print full header nicely ---
print("=== Full OWON Header ===")
print(json.dumps(header, indent=4))
print("="*40)

# --- Extract channel identifiers ---
hdr_end = end + 1
n_channels = len(header.get("channel", []))
ch_id = blob[hdr_end:hdr_end+4]
hdr_end += 4

print(f"Found {n_channels} channel ID: {ch_id.hex(' ')}")

raw16 = blob[hdr_end:hdr_end+32]
# print first few samples of data in hex
print("Data start (hex):", raw16[:32].hex(' '))

# prepare MDF container to collect channel signals
mdf = MDF()
out_mdf = os.path.splitext(file_path)[0] + '.mf4'

# --- Extract waveform data per channel ---
for ch_idx, ch in enumerate(header.get("channel", [])):
    print(f"\n--- Channel {ch_idx+1} ({ch.get('Index','?')}) ---")
    n_samples = int(ch.get("Data_Length"))
    ref_zero = int(ch.get("Reference_Zero"))
    v_rate = float(ch.get("Voltage_Rate").replace("mv",""))*1e-3

    probe = float(ch.get("Probe_Magnification").replace("X",""))
    adc_dt = float(ch.get("Adc_Data_Time").replace("us",""))*1e-6

    # waveform start after header + channel IDs
    data_start = hdr_end
    data_end = data_start+n_samples*2
    data_end_file = len(blob)
    raw16 = blob[data_start:data_end_file]
    raw16 = raw16[:len(raw16)]
    # little endian
    # scope stores as a int16_t so need to interpret as such
    dt = np.dtype(np.int16)
    dt = dt.newbyteorder("<")
    counts = np.frombuffer(raw16, dtype=dt)

    #first count
    print("First 16 samples:", counts[:16])

    # print start of data in hex
    print("Data start (hex):", raw16[:32].hex(' '))

    # make 32bit int counts
    counts32 = counts.astype(np.int32)
    # --- Voltage scaling using header fields ---
    volts = (counts32 - ref_zero*128) * v_rate * probe

    # --- Time axis ---
    t = np.arange(len(volts)) * adc_dt

    # --- Append channel to MDF ---
    sig_name = f"{ch.get('Index','CH')}_{ch_idx+1}"
    try:
        mdf.append(Signal(samples=np.asarray(volts, dtype=float),
                          timestamps=np.asarray(t, dtype=float),
                          name=sig_name,
                          unit='V'))
        print(f"Appended signal to MDF: {sig_name} (samples={len(volts)})")
    except Exception as e:
        print(f"Failed to append signal {sig_name} to MDF:", e)

    # --- Plot full waveform with sample marker ---
    # plt.rcParams["agg.path.chunksize"] = 1000
    # plt.figure(figsize=(12,4))
    # plt.plot(t, volts, lw=1, label='Waveform')
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")
    # plt.title(f"Channel {ch_idx+1}: {ch.get('Index','?')}")
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

    # make asammdf file

# save MDF after processing all channels
try:
    mdf.save(out_mdf, overwrite=True)
    print("Saved MDF:", out_mdf)
except Exception as e:
    print("Failed to save MDF:", e)

