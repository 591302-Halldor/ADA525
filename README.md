# ADA525
ADA525 project


I created a stationary robot capable of horizontally and vertically moving a camera to center a detected face. The Arduino Uno controls a stepper motor for horizontal movement and a servo motor for vertical movement. A Raspberry Pi 3 hosts the facial recognition software using OpenCV. A Python script on the Raspberry Pi manages system logic, providing directional distance information to the Arduino for power regulation. The Raspberry Pi also addresses delay issues to prevent camera overshooting.
 
