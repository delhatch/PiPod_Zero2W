# PiPod_Zero2W
This project started as a clone of https://github.com/BramRausch/PiPod
<H3>Motivation</H3>
<p>I created this version to:</p>
<ul><li>Change from the Raspberry Pi Zero to the Pi Zero 2 W.</li>
<li>To document all of the steps necessary to create the PiPod from scratch, starting with a new Pi Zero 2 W</li></ul>
<H3>Benefits</H3>
<ul><li>The wifi of the Pi 2 W makes for easy software installation (sudo apt) and updates</li>
<li>Easy to transfer music files, via SFTP over wifi, from a laptop to the PiPod (using WinSCP for example).</li>
<li>Because a USB breakout hub is used to connect a keyboard & mouse, it is also easy to plug in a USB Flash drive to load or move files.</li></ul>
<H3>Hardware changes</H3>
<ul><li>Increase R6 to 3.75 kOhm to reduce the battery charging current to 325 mA (= 0.28C)</li>
<li>Increase R9 to 4.7 kohm to reduce the brightness of the green LED</li></ul>
<H3>Software Changes</H3>
<ul><li>Instead of using Retrogame to link the UI buttons to the pygame event que, I use a callback function (triggered by the GPIO change) that posts an event to the pygame event que. (See device.py. Ugly, I know, but efficient and gives fine-grained control for future features such as press-and-hold functions.)</li><li>Instead of using pygame to flush the frame buffer to the LCD (/dev/fb1), it is done "manually." This allows you to have the Pi 2W HDMI output connected to a large monitor, while still running the PiPod software updating its small LCD.</li></ul>
<H3>THIS PROJECT IS CURRENTLY UNDER ACTIVE DEVELOPMENT!</H3>
<p>Lots of things are changing daily as I adapt the software, and what the developer needs to do to make it all work together.</p>
