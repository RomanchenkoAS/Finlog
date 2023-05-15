import sys
import time

def animate_arrow():
    # Define the number of characters for the arrow animation
    num_chars = 20
    # Define the initial position of the arrow
    pos = 0
    # Define the direction of the arrow
    direction = 1
    
    while True:
        # Create the string for the arrow animation
        s = "installation ({}{})".format("=" * pos, ">" if direction == 1 else "<" * (-direction))
        # Print the arrow animation to the console
        sys.stdout.write("\r" + s)
        sys.stdout.flush()
        
        # Update the position and direction of the arrow
        pos += direction
        if pos == num_chars:
            direction = -1
        elif pos == 0:
            direction = 1
        
        # Wait for a short time before the next iteration
        time.sleep(0.1)

# Call the animate_arrow function to start the animation
animate_arrow()
