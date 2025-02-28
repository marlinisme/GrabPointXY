import cv2

# Global variables to store points and boundaries
points = []
boundaries = {}
reference_point = None
boundary_names = ["Boundary1", "Boundary2", "Boundary3", "Boundary4"]  # Names for the boundaries
current_boundary_index = 0  # Track which boundary is being selected
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Colors for each boundary

# Function to display the coordinates of the points clicked on the image
def click_event(event, x, y, flags, params):
    global points, reference_point, img

    # Checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # If reference point is not set, set it as (x=0, y=0)
        if reference_point is None:
            reference_point = (x, y)
            print(f"Reference point set at: {reference_point}")
        else:
            # Adjust the clicked point relative to the reference point
            adjusted_x = x - reference_point[0]
            adjusted_y = y - reference_point[1]
            points.append((adjusted_x, adjusted_y))
            print(f"Adjusted point: ({adjusted_x}, {adjusted_y})")

            # Draw a dot mark at the clicked point
            color = colors[current_boundary_index]  # Use the current boundary's color
            cv2.circle(img, (x, y), 3, color, -1)  # Draw a small filled circle
            cv2.imshow('image', img)

# Function to save a single boundary to a text file
def save_boundary(boundary_name, boundary_points):
    filename = f"{boundary_name}.txt"
    with open(filename, 'w') as file:
        file.write(f"{boundary_points}\n")
    print(f"Boundary '{boundary_name}' saved to '{filename}'.")

# Function to load a single boundary from a text file
def load_boundary(boundary_name):
    filename = f"{boundary_name}.txt"
    try:
        with open(filename, 'r') as file:
            points_str = file.read().strip()
            points = eval(points_str)  # Convert string representation of list to actual list
            boundaries[boundary_name] = points
        print(f"Boundary '{boundary_name}' loaded from '{filename}'.")
        print(f"{boundary_name}: {points}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error loading boundary '{boundary_name}': {e}")

# Driver function
if __name__ == "__main__":
    # Display instructions in the console
    print("=== Boundary Selection Program ===")
    print("Instructions:")
    print("1. Click on the image to set the reference point (x=0, y=0).")
    print("2. Click to select points for the current boundary.")
    print("3. Press the SPACEBAR to save the current boundary and start a new one.")
    print("4. Press ENTER to finish the process and save all boundaries.")
    print("5. Each boundary will be saved to a separate text file.")
    print("=================================")

    # Reading the image
    img = cv2.imread('ChestCT-Scan_images_0.png', 1)
    if img is None:
        print("Error: Image not found. Please check the file path.")
        exit()
    original_img = img.copy()  # Keep a copy of the original image

    # Displaying the image
    cv2.imshow('image', img)

    # Setting mouse handler for the image and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    while True:
        key = cv2.waitKey(1) & 0xFF

        # Save the current boundary when spacebar is pressed
        if key == ord(' '):
            if points:
                # Save the current points with a meaningful name
                boundary_name = boundary_names[current_boundary_index]
                boundaries[boundary_name] = points
                print(f"\nBoundary saved as '{boundary_name}': {points}")
                print(f"Now you can select points for the next boundary.")
                print("Press SPACEBAR again to save the next boundary or ENTER to finish.\n")

                # Save the current boundary to a separate file
                save_boundary(boundary_name, points)

                points = []  # Reset points for the next boundary
                current_boundary_index += 1  # Move to the next boundary

                # Stop if all boundaries are saved
                if current_boundary_index >= len(boundary_names):
                    print("All boundaries have been saved.")
                    break
            else:
                print("No points selected for the current boundary. Please select points before saving.")

        # Exit the loop and finish the process when Enter is pressed
        if key == 13:  # 13 is the ASCII code for Enter
            if points:
                # Save the final boundary if there are unsaved points
                boundary_name = boundary_names[current_boundary_index]
                boundaries[boundary_name] = points
                print(f"\nFinal boundary saved as '{boundary_name}': {points}")

                # Save the final boundary to a separate file
                save_boundary(boundary_name, points)
            break

    # Close the window
    cv2.destroyAllWindows()

    # Print all boundaries with their names
    print("\n=== All Boundaries ===")
    for name, boundary in boundaries.items():
        print(f"{name}: {boundary}")