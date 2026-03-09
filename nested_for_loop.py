import bpy

# time consuming

# 10*10*10
count = 10

# triple for-loop: time consuming 
for i in range (count):
    for j in range (count):
        for k in range (count):
            x = i*2
            y = j*2
            z = k*2
            bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
