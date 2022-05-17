from scene import Scene
import taichi as ti
from taichi.math import *

day = False
scene = Scene(voxel_edges=0, exposure=1)
scene.set_floor(-1, (1.15, 1.4, 1.9) if day else ((0.01, 0.01, 0.02)))
scene.set_background_color((0.9, 0.98, 1) if day else (0.01, 0.01, 0.02))
scene.set_directional_light((.6, .75, 1), 0.1, (1.1, .95, 0.75) if day else (.3, .3, 0.5))

@ti.func
def create_sphere(pos, radius, m, c):
    for I in ti.grouped(ti.ndrange((-radius, radius), (-radius, radius), (-radius, radius))):
        if I.norm() < radius:
            scene.set_voxel(pos + I, m, c)

@ti.func
def draw_table():
    for x, z in ti.ndrange ((-64, 64),(-64, 64)):
        h = 7 * ti.sin(ti.cast(x, ti.f32) / 50 * 3.14) * ti.sin(ti.cast(z , ti.f32)/45 * 3.14)
        scene.set_voxel(vec3(x, -64, z), 1, vec3(0.3, 0.5, 0.7))

@ti.func
def draw_vase(center, radius, step):
    for i, y in ti.ndrange ((-step, step),(-64, 0)):
        l = 1
        r = ti.cast(i, ti.f32) / step * 3.14
        w = 8 * ti.sin(ti.cast(i, ti.f32) / 50 * 3.14) * ti.sin(ti.cast(y , ti.f32)/55 * 3.14) + 15
        c = mix(vec3(0.5, 0.6, 0.7), vec3(1.0, 0.6, 0.6), (y+64)/64)
        d = 10 * ti.sin(ti.cast(i, ti.f32) / 88 * 3.14) * ti.sin(ti.cast(y , ti.f32)/150 * 3.14) + 14
        if w < d:
            l = 2
        scene.set_voxel(vec3(ti.cast(w * ti.sin(r), ti.i32)+ center.x, y, ti.cast(w * ti.cos(r), ti.i32) + center.y), l, c)

@ti.func
def draw_flower(center, size):
    for i in range(0,200):
        v = vec3(ti.random()*2-1,ti.random()*2-1,ti.random()*2-1)
        for j in range(0,size):
            pos = center + v*j
            c = mix(vec3(.9, .8, 0.5), vec3(1.3, 1.2, 1.1), j/20)
            if distance(center,pos) < size-5:
                scene.set_voxel(pos, 1, c)
    if day==False:
        create_sphere(center, size/5, 2, vec3(10, .6, .2))

@ti.func
def draw_stem(posA, posB, posC, step):
    for i in range(0,step):
        x = pow(1 - i/step, 2) * posA.x + (1 - i/step) * 2 * i/step * posB.x + i/step * i/step * posC.x 
        y = pow(1 - i/step, 2) * posA.y + (1 - i/step) * 2 * i/step * posB.y + i/step * i/step * posC.y 
        z = pow(1 - i/step, 2) * posA.z + (1 - i/step) * 2 * i/step * posB.z + i/step * i/step * posC.z 
        scene.set_voxel(vec3(x,y,z), 1, vec3(0.15,0.3,0.05))

        if i == 7:
            create_sphere(vec3(x,y,z), 3, 1, vec3(0.15,0.3,0.05))

@ti.func
def draw_wall():
    for i, j in ti.ndrange((-64,64), (-64,64)):
        w = 8 * ti.sin(ti.cast(i, ti.f32) / 50 * 3.14) * ti.sin(ti.cast(j , ti.f32)/45 * 3.14) + 35
        c = mix(vec3(.5, .9, 0.5), vec3(.35, 0.55, .95), (i+64)/128)
        if i < w and (w - i * .7) % 5 > 2 :
            scene.set_voxel(vec3(i, j, -64), 2, c)
            scene.set_voxel(vec3(-64, j, i), 2, c)


@ti.func
def draw_particles(num):
    for i in range(0, num):
        x = mix(-64, 64, ti.random())
        z = mix(-64, 64, ti.random())
        scene.set_voxel(vec3(x,-63,z), 2, vec3(ti.random()*0.3 + 0.7, ti.random()*0.3 + 0.55,0.5))


@ti.kernel
def initialize_voxels():
    draw_table()
    draw_vase(vec2(-20,-20), 32, 100)
    draw_particles(100)
    draw_wall()
    draw_flower(vec3(12, -55, 39), 15); draw_stem(vec3(12, -55, 39), vec3(-70, -64, 40), vec3(-35, -62, -55), 200)
    draw_flower(vec3(45, -30, -37), 15); draw_stem(vec3(45, -30, -37), vec3(0, 30, -30), vec3(-28, -5, -25), 200)
    draw_flower(vec3(40, -5, 40), 18); draw_stem(vec3(40, -5, 40), vec3(-30, 100, -20), vec3(-20, -64, -20), 200)
    draw_flower(vec3(-40, 52, -35), 18); draw_stem(vec3(-40, 52, -35), vec3(0, 80, 0), vec3(-25, -64, -20), 200)
    draw_flower(vec3(0, 40, 10), 30); draw_stem(vec3(0, 40, 10), vec3(-35, 10, -32), vec3(-15, -64, -25), 200)
    draw_flower(vec3(30, 25, 30), 20); draw_stem(vec3(30, 25, 30), vec3(-25, 50, -30), vec3(-17, -64, -23), 200)
    draw_flower(vec3(10, 5, -20), 26); draw_stem(vec3(10, 5, -20), vec3(-30, 20, -10), vec3(-22, -64, -27), 200)
    draw_flower(vec3(-40, 13, 40), 25); draw_stem(vec3(-40, 13, 40), vec3(-20, 40, -20), vec3(-25, -64, -22), 200)

initialize_voxels()

scene.finish()
