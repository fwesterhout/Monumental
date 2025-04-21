# Monumental

Please try the 2 uploaded Python files to visualize building a wall.

## Monumental-zigzag-method.py

In this python script, I focused on minimizing the amount of strides. With the defined build-envelope and wall dimension this resulted in 6 strides. 

To run this python file, open the file in your terminal and run " python Monumental-zigzag-method.py ". This will open an interactrive pygame window, which expects user input. Every time the user presses "ENTER", one brick is added to the wall, until the wall is completely finished. 

## Monumental-stair-method.py

Here, I focused on a more realistic method and this script is intended to show an alternative technique. As 1 stride of the robot is only covering 3.5 bricks in width, more strides are needed to finish the wall in this way. The benefit is that the brick-laying pattern is not disturbed. A visualisation is given of only the first 3 strides, as this showcases the fact that it is much slower but more realistic. 

To run this python file, open the file in your terminal and run " python Monumental-stair-method.py ". This will open an interactrive pygame window, which expects user input. Every time the user presses "ENTER", one brick is added to the wall, until 3 strides are finished.

Have fun building!
