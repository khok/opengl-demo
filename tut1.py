# Mario Rosasco, 2016
# adapted from tut1.cpp, Copyright (C) 2010-2012 by Jason L. McKesson
# This file is licensed under the MIT License.

from OpenGL.GL import *
from array import array
import numpy as np
from framework import createShader, createProgram
import cyglfw3 as glfw
from time import time, sleep

# A 1-D array of 3 4-D vertices (X,Y,Z,W)
# Note that this must be a numpy array, since as of 
# 170111 support for lists has not been implemented.
vertexPositions = np.array(
    [-1, -1, 0.0, 1.0,
    0, 1, 0.0, 1.0, 
    1, -1, 0.0, 1.0],
    dtype='float32'
)

vertexDim = 4
nVertices = 3

# String containing vertex shader program written in GLSL
strVertexShader = """
#version 330

uniform float myPos;

layout(location = 0) in vec4 position;
void main()
{
   gl_Position = vec4(position.x * myPos, position.y * myPos, 0.0, 1.0);
}
"""

# String containing fragment shader program written in GLSL
strFragmentShader = """
#version 330

uniform vec2 heartCenter;

out vec4 outputColor;

void drawHeart(float x, float y)
{
    float f = x*x + y*y - 2000;

    float val = f*f*f - 40*x*x*y*y*y;

   //float val = 10*x + 5 - y;

    float res = float(val < 0);

    outputColor = vec4(1.0f * res , 1.0f * (1 - res), 0.0f, 1.0f);    
}

void main()
{
   vec2 pos = gl_FragCoord.xy - heartCenter;
   drawHeart(pos.x, pos.y);
}
"""

# Global variable to represent the compiled shader program, written in GLSL
theProgram = None

# Global variable to represent the buffer that will hold the position vectors
vao = None



# Set up the list of shaders, and call functions to compile them
def initializeProgram():
    shaderList = []
    
    shaderList.append(createShader(GL_VERTEX_SHADER, strVertexShader))
    shaderList.append(createShader(GL_FRAGMENT_SHADER, strFragmentShader))
    
    global theProgram 
    theProgram = createProgram(shaderList)
    
    for shader in shaderList:
        glDeleteShader(shader)

# Set up the vertex buffer that will store our vertex coordinates for OpenGL's access
def initializeVertexBuffer():
    vbo = glGenBuffers(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData( # PyOpenGL allows for the omission of the size parameter
        GL_ARRAY_BUFFER,
        vertexPositions,
        GL_STATIC_DRAW
    )
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo

def initializeVertexArray(vbo):
    vao = glGenVertexArrays(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glVertexAttribPointer(0, vertexDim, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    return vao


# Initialize the OpenGL environment
def init():
    global vao
    initializeProgram()
    vao = initializeVertexArray(initializeVertexBuffer())

# Called to update the display. 
# Because we are using double-buffering, glutSwapBuffers is called at the end
# to write the rendered buffer to the display.

anim = 0.0
dirc = 1

def display(window):
    global anim, dirc
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glUseProgram(theProgram)

    unif = glGetUniformLocation(theProgram, 'myPos')
    glUniform1f(unif, anim)

    # glUniform1f(unif, anim)

    x, y = glfw.GetFramebufferSize(window)

    unif = glGetUniformLocation(theProgram, 'heartCenter')
    glUniform2f(unif, x / 2, y / 2)

    # anim += 0.1 * dirc

    # if anim > 1 or anim < 0:
        # dirc *= -1

    anim = 1

    glBindVertexArray(vao)

    glEnableVertexAttribArray(0)
    glDrawArrays(GL_TRIANGLES, 0, nVertices)
    glDisableVertexAttribArray(0)

    glUseProgram(0)
    glBindVertexArray(0)


# keyboard input handler: exits the program if 'esc' is pressed
def keyboard(key, x, y):
    if ord(key) == 27: # ord() is needed to get the keycode
        glutLeaveMainLoop()
        return
    
# Called whenever the window's size changes (including once when the program starts)
def window_size_callback(window, width, height):
    glViewport(0, 0, width, height)

# The main function
def main():

    glfw.Init()
    # version hints
    glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.CreateWindow(800, 600, "First App");

    glfw.MakeContextCurrent(window);

    glfw.SetWindowSizeCallback(window, window_size_callback);

    try:
        init()
    except Exception as e:
        print(e)
        exit(1)

    prevTime = time()

    timeSum = 0
    count = 0

    while not glfw.WindowShouldClose(window):
        glfw.PollEvents();
        display(window)
        glfw.SwapBuffers(window);

        curTime = time()

        # print(curTime - prevTime)
        # count += 1
        # timeSum += curTime - prevTime
        prevTime = curTime
        sleep(0.016)


    # print(count / timeSum)
    glfw.Terminate();

if __name__ == '__main__':
    main()
