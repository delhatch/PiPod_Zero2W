# PiPod_Zero2W
This project started as a clone of https://github.com/BramRausch/PiPod
<H3>Motivation</H3>
<p>I created this version to:</p>
<ul><li>Change from the Raspberry Pi Zero to the Pi Zero 2 W.</li>
<li>To document all of the steps necessary to create the PiPod from scratch, starting with a new Pi Zero 2 W.</li></ul>
<H3>Benefits</H3>
<ul><li>The wifi of the Pi 2 W makes for easy software installation (sudo apt) and updates.</li>
<li>Easy to transfer music files, via SFTP over wifi, from a laptop to the PiPod (using WinSCP, for example.)</li>
<li>Because a USB breakout hub is used to connect a keyboard & mouse, it is also easy to plug in a USB Flash drive to load or move files.</li></ul>
<H3>Hardware changes</H3>
<ul><li>Increase R6 to 3.75 kohm to reduce the battery charging current to 325 mA. This is a 0.28C charge rate (instead of 1C charging) which increases the battery's life.</li>
<li>Increase R9 to 4.7 kohm to reduce the brightness of the green LED</li></ul>
<H3>Software Changes</H3>
<ul><li>Instead of using Retrogame to link the UI buttons to the pygame event que, I use a callback function (triggered by the GPIO change) that posts an event to the pygame event que. (See device.py)</li><li>Instead of using pygame to flush the frame buffer to the LCD (/dev/fb1), it is done "manually." This allows you to have the Pi 2 W HDMI output connected to a large monitor, while still running the PiPod software updating its small LCD.</li></ul>
<H3>THIS PROJECT IS CURRENTLY UNDER ACTIVE DEVELOPMENT!</H3>
<p>Lots of things are changing daily as I adapt the software, and what the developer needs to do to make it all work together.</p>
<H2>Hardware Parts</H2>
<p>You will need to buy the bare PCB from https://www.pcbway.com/project/shareproject/PiPod___Raspberry_pi_Zero_portable_music_player.html</p>
<p>Populate it with components as described in the original PiPod project. Some sources for critical components are listed below for convenience:</p>
<ul><li>The only source I can find for the 2.2" LCD (Tianma TM022HDH26 with ILI9340C/ILI9341 driver IC) is Adafruit, item #1480.</li>
<li>The LiPo battery measures xxx. One source is yyy.</li>
<li>The headphone jack is Digikey part CP-SJ2-3573A2-SMT-CT-ND</li>
<li>The SMPS inductor (L1) is Digikey part 732-2617-1-ND</li>
<li>The 40-pin connector for the Pi Zero 2 W is Digikey part 609-2231-ND</li>
<li>The sliding power switch is Digikey part EG1903-ND</li>
<li>The small USB connector is Digikey part 609-4616-1-ND</li>
<li>The side-mount pushbutton switches are Digikey part 609-4616-1-ND</li>
<li>The red and green LEDs are Digikey part 1830-1082-1-ND and 1830-1079-1-ND, respectively</li></ul>
<H2>Instructions</H2>

