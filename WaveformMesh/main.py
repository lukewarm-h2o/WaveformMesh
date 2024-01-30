"""///////////////////////////////////////////////
    .mp3 -> .stl Waveform visualizer tool

    Luke Bopp-art 2024
    MIT licence
///////////////////////////////////////////////"""
import math
import librosa
import matplotlib.pyplot as plt
import numpy as np
from stl import mesh
'''
Ensure you have the numpy-stl library installed. You can install it via pip:

`bash
   > pip install numpy-stl

'''


def create_box(position, scale):
    """
    Create a box mesh with given position and scale.

    :param position: A list or array with 3 elements [x, y, z] for position.
    :param scale: A list or array with 3 elements [x, y, z] for scale.
    :return: A mesh object representing the box.
    """
    # Define the 8 vertices of the box
    vertices = np.array([
        [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]
    ])

    # Scale and position the vertices
    vertices *= scale
    vertices += position

    # Define the 12 triangles composing the box
    faces = np.array([
        [0, 3, 1], [1, 3, 2], [0, 4, 7], [0, 7, 3],
        [4, 5, 6], [4, 6, 7], [5, 1, 2], [5, 2, 6],
        [2, 3, 6], [3, 7, 6], [0, 1, 5], [0, 5, 4]
    ])

    # Create the mesh
    box = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            box.vectors[i][j] = vertices[f[j], :]

    return box


def add_boxes_to_stl(positions, scales, filename="output.stl"):
    """
    Create an STL file with boxes at specified positions and scales.

    :param positions: A list of positions, each a list or array of 3 elements.
    :param scales: A list of scales, each a list or array of 3 elements.
    :param filename: The name of the output STL file.
    """
    assert len(positions) == len(scales), "Positions and scales arrays must be of equal length."

    # Combine all boxes into one mesh
    combined_mesh = mesh.Mesh(np.concatenate([create_box(pos, scale).data for pos, scale in zip(positions, scales)]))

    # Save to file
    combined_mesh.save(filename)


def downsample_audio(audio, num_points):
    # Downsample the audio to a specified number of points
    downsampled_audio = np.interp(np.linspace(0, len(audio), num_points), np.arange(len(audio)), audio)
    return downsampled_audio


def split_audio(audio, num_rows):
    # Split the audio into equal length segments
    length = len(audio)
    segment_length = length // num_rows
    return [audio[i*segment_length:(i+1)*segment_length] for i in range(num_rows)]

def plot_waveform(file_path):
    # Load the audio file
    audio, sr = librosa.load(file_path, sr=None)

    # Plot the waveform
    plt.figure(figsize=(14, 5))
    plt.plot(audio)
    plt.title('Waveform of the Audio')
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.show()

    return audio



if __name__ == '__main__':

    # put the file path to an mp3 here
    audio_path = 'Therapy feat. Visious & Defiant (Prod. By Swedo Beats).mp3'

    # adjust the number of points to down-sample to
    num_points = 8000  # Adjust this to your desired number of points for down-sampling
    grid_dimensions = int(math.sqrt(num_points))
    audio_data = plot_waveform(audio_path)
    downsampled_audio = downsample_audio(audio_data, num_points)
    wave_slice = split_audio(downsampled_audio, num_rows=grid_dimensions)  # Replace with your desired number of rows

    '''
    Direct Meshing
    '''
    print("Rows:")
    print(len(wave_slice))
    print("Columns:")
    print(len(wave_slice[0]))
    box_positions = []
    scales = []

    for x in range(len(wave_slice)):
        for y in range(len(wave_slice[x])):
            z = wave_slice[x][y]
            box_positions.append([x * 10, y * 10, 0])
            scales.append([10, 10, 1 + z * 100])

    print("adding boxes now")
    add_boxes_to_stl(box_positions, scales, "waveform.stl")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
