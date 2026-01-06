# Vision-Based Target Tracking (OpenCV)

This project implements a real-time vision-based target tracking system
using OpenCV. The system detects a red-colored target, calculates its
horizontal offset from the camera center, and generates yaw direction
decisions similar to UAV guidance logic.

## Features
- HSV-based color segmentation
- Morphological noise removal
- Largest contour selection
- Target center calculation
- Direction decision based on error tolerance

## Technologies
- Python
- OpenCV
- NumPy

## Use Case
This structure is suitable for:
- UAV vision guidance systems
- Target tracking applications
- Pre-PID control logic in autonomous drones

## Future Improvements
- PID controller integration
- MAVLink yaw command output
- Gazebo / SITL simulation support
