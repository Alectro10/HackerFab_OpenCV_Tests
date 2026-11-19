
import serial

# target position in camera pixels
target_x = 800
target_y = 400

# detected pattern position in camera pixels
current_x = 850
current_y = 420

# camera calibration
# example values only, replace after testing
mm_per_pixel_x = 0.01
mm_per_pixel_y = 0.01

# stage direction from calibration
x_direction = 1
y_direction = 1

# maximum movement allowed per command in mm
max_move = 0.5

# keep false until the stage is calibrated
move_stage = False

# calculate the pixel difference
error_x = target_x - current_x
error_y = target_y - current_y

# convert pixels to mm
move_x = error_x * mm_per_pixel_x * x_direction
move_y = error_y * mm_per_pixel_y * y_direction

print("Current position:", current_x, current_y)
print("Target position:", target_x, target_y)

print("X error:", error_x, "pixels")
print("Y error:", error_y, "pixels")

print("Move X:", move_x, "mm")
print("Move Y:", move_y, "mm")

# prepare movement command
command = f"$J=G91 G21 X{move_x:.4f} Y{move_y:.4f} F50"

print("Movement command:", command)

# check movement limits
safe_move = (
    abs(move_x) <= max_move
    and abs(move_y) <= max_move
)

if not safe_move:
    print("Movement exceeds allowed limit")

elif not move_stage:
    print("Simulation only - stage will not move")

else:
    # change this to the actual controller port
    port = "/dev/cu.usbmodemXXXX"

    confirm = input("Send movement command? (yes/no): ")

    if confirm == "yes":
        with serial.Serial(port, 115200, timeout=2) as stage:
            stage.write((command + "\n").encode())
            response = stage.readline().decode(errors="replace")
            print("Controller response:", response)
    else:
        print("Movement cancelled")
