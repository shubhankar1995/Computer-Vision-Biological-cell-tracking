The application is intended to be run using Python 3.7+.
Run main.py to launch the application.
The parameters of the application are sequence_directory and mode.
sequence_directory is the relative path to directory containing the sequence of images.
The mode parameter chooses the preprocessing and segmentation methods to be used, which depends on the imageset.
Modes: 0 -> DIC-C2DH-HeLa, 1 -> Fluo-N2DL-HeLa, 2 -> PhC-C2DL-PSC

Examples:
python3 main.py path/to/DIC/sequence 0 
python3 main.py path/to/Fluo/sequence 1 
python3 main.py path/to/PhC/sequence 2
