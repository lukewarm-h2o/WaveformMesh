# WaveformMesh
A minimal python script for turning .mp3 files into an arrangement of box meshes


## Usage
Start by providing an mp3 file path to the audio_path variable near the bottom of the main.py script,
then you can run the script to generate the box-grid representation.
### to adjust  the look of the output you can adjust:
- `num_points` sets the total number of samples/boxes
- `num_rows` set the number of rows to arrange the boxes into (calculates square dimensions by default)
- `box_positions.append([x * 10, y * 10, 0])` chage the *10 scale to space boxes tighter or further
- `scales.append([10, 10, 1 + z * 100])` chages the scale of the individual boxes (z = Waveform Amplitude)


## Note
meshes use right hand coordinate system with +z = up
