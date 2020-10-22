# paint-magic
A painting tool that generates inverse "snapped" effect using linear interpolation.

![sample](https://i.imgur.com/vr2pmTU.gif)

## Requirements
  * `Python 3.6.x` or higher
  * `pygame 1.9.x` or higher
  * `Pillow 8.x` or higher. (Not necessary, but required to save the animation as a GIF)

## How to use:
`Left Mouse Button`         : Paint pixels <br>
`Right Mouse Button`        : Erase pixels <br>
`Right and Left arrow keys` : change colors <br>
`Up and Down arrow keys`    : change brush size <br> 
`Spacebar`                  : Play or repeat the animation. 

## Features:
 * Highly configurable
 * Can output the animation as a .GIF with various level of smoothness using ``optimization-level`` parameter (WIP)
