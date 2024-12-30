# Bedslinger_Gantry_Alignment
Simple plugin to align your Z gantry to printer's frame.
<TODO> Youtube video

## Hardware configuration
Your Z gantry needs to be controlled by at least two independently controlled stepper motors (have at least stepper_z and stepper_z1 configured in printer.cfg).
You also need additional endstop for each independently controlled Z stepper motor.

Assuming you're using probe to home Z, mount newly added endstops on the top of printer's frame so they won't disturb normal operation of the printer. Each endstop should be able to touch Z gantry during alignment. Also each endstop should be as close as possible to it's corresponding stepper's leadscrew.

<TODO> Example picture

## Installation
```
cd ~
git clone https://github.com/Tai-Min/Bedslinger_Gantry_Alignment
cd Bedslinger_Gantry_Alignment && ./install.sh
```

## Configuration
printer.cfg:
```
# Force move must be present in printer.cfg!
[force_move]
enable_force_move: true # Doesn't matter whether true or false

[bedsligner_gantry_alignment]
z_endstops: ^PC13, ^PC2 # Endstops for stepper_z, stepper_z1 ... stepper_zn.
safe_x_pos: 117.5 # Safe position of X gantry that won't crash into alignment endstops, on typical 3d printers it's the center of workspace.
initial_z_height: 220 # Fast move to adjustment position. Move as close as possible to adjustment endstops without triggering them to save time.
initial_move_speed: 10 # mm/s

align_step_size_initial: 0.2 # mm, too large value might damage the printer!
align_step_size_precise: 0.1 # Same as above
align_backtrack: 1.5 # mm, backtrack distance before precise alignment, the value must be high enough to clear endstops.
align_step_speed: 5
align_step_accel: 100

# Fast backtrack movement after adjustment. Usually making it equal to initial_z_height is okay.
# In that case gantry will be lowered to roughly it's initial position (but not the same as the Z axis position
# will be invalid after adjustment! new Z homing operation IS REQUIRED)
backtrack_distance: 220 
```

Sample macro:
```
[gcode_macro LEVEL_GANTRY]
description: Adjust gantry to frame
gcode:
    {% if "xyz" not in printer.toolhead.homed_axes %}
        G28
    {% endif %}

    BEDSLINGER_GANTRY_ALIGN

    G28 Z
```

Moonraker:
```
[update_manager Bedslinger_Gantry_Alignment]
type: git_repo
path: ~/Bedslinger_Gantry_Alignment
origin: https://github.com/Tai-Min/Bedslinger_Gantry_Alignment
primary_branch: master
```

## Usage
Script in Configuration section is pretty much all required. If you want to utilize this plugin to your own printing routine then remember that:
* All axes must be homed before BEDSLINGER_GANTRY_ALIGN
* Z axis must be homed again after BEDSLINGER_GANTRY_ALIGN
* During manual bed level make sure BEDSLINGER_GANTRY_ALIGN is called before to level the bed to aligned gantry

## Disclaimer
I've tested this plugin only on my configuration (Ender 3 frame, config as in above exapmpe). 
I'm not sure how it would behave with in example inverted endstops. Before putting your faith this plugin, make sure to test it properly, by triggering the endstops by hand first and/or running the script with your hand on Emergency Stop button to prevent any damage. 

Use at your own risk.
