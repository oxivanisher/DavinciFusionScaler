# DavinciFusionScaler
Scales keyframes in Davinci Resolve Fusion .settings files (go from 30 to 60 FPS with ease...)

Please be aware, that this script is pretty stupid. It just searches for lines containing `KeyFrames = {` and increases
or decreases the number within `[ ]` by the multiplier, until the corresponding `}` line for the KeyFrames line is found.
