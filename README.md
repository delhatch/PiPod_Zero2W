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
<ul><li>Increase R6 to 3.75 kohm to reduce the battery charging current to 325 mA. This is a 0.28C charge rate (instead of 1C charging) which helps to increase the battery's life.</li>
<li>Increase R9 to 4.7 kohm to reduce the brightness of the green LED</li></ul>
<H3>Software Changes</H3>
<ul><li>Instead of using Retrogame to link the UI buttons to the pygame event que, I use a callback function (triggered by the GPIO change) that directly posts an event to the pygame event que. (See device.py)</li>
<li>Instead of using the pygame.display.update() method to flush the frame buffer to the LCD at /dev/fb1, it is now done "manually." (See the refresh() method in display.py) This allows you to simultaneously have the Pi 2 W HDMI output connected to a large monitor, while still running the PiPod software updating its small LCD.</li>
<li>Fixed an issue where the MP3 file would not appear in the library if the "ALBUM" field was blank. It now inserts the album title "Not Sure" and continues.</li></ul>
<H3>THIS PROJECT IS CURRENTLY UNDER ACTIVE DEVELOPMENT!</H3>
<p>Lots of things are changing daily as I adapt the software, and what the developer needs to do to make it all work together.</p>
<H2>Hardware Parts</H2>
<p>You will need to purchse a bare PCB from https://www.pcbway.com/project/shareproject/PiPod___Raspberry_pi_Zero_portable_music_player.html</p>
<p>Populate it with components as described in the original PiPod project. Some sources for critical components are listed below for convenience:</p>
<ul><li>The Pi Zero 2 W is a direct drop-in replacement for the PiPod's original Pi Zero.</li>
<li>The only source I can find for the 2.2" LCD (Tianma TM022HDH26 that has the ILI9340C/ILI9341 driver IC) is Adafruit, item #1480.</li>
<li>The LiPo 1200mAh battery measures 34mm x 62mm x 5mm / 1.3" x 2.4" x 0.2". One source is Adafruit #258.</li>
<li>The headphone jack is Digikey part CP-SJ2-3573A2-SMT-CT-ND</li>
<li>The SMPS inductor (L1) is Digikey part 732-2617-1-ND</li>
<li>The 40-pin connector for the Pi Zero 2 W is Digikey part 609-2231-ND</li>
<li>The sliding power switch is Digikey part EG1903-ND</li>
<li>The small USB connector is Digikey part 609-4616-1-ND</li>
<li>The side-mount pushbutton switches are Digikey part EG4388CT-ND</li>
<li>The red and green LEDs are Digikey part 1830-1082-1-ND and 1830-1079-1-ND, respectively</li></ul>
<H2>Instructions</H2>
<ul><li>Download the OS file "2023-12-05-raspios-bookworm-arm64.img.xz</li>
<li>Using rufus-3.22 (or similar), burn the image to a 128GB micro-SD card.</li>
<li>Assuming you have a fully-assembled PiPod hardware: Connect an HDMI monitor to the Pi Zero 2 W. Also connect a USB expander hub such as the SmartQ
H302S to the Pi Zero usb connector. Connect a USB keyboard and mouse to the hub.</li>
<li>Power-up the Pi Zero and go through the configuration screens. Make sure wifi is enabled and connect to a network. Reboot.</li>
<li>Type sudo nano /boot/config.txt and make the following changes:
  <ul>
    <li>un-comment dtparam=spi=on (to turn on the SPI port)</li>
    <li>comment-out the "dtparam=audio=on" line</li>
    <li>add a line: dtoverlay=hifiberry-dac</li>
    <li>un-comment dtparam=i2c_arm=on</li>
    <li>at the bottom of the file, add the lines:</li>
    <ul>
      <li>dtoverlay=fbtft,spi0-0,ili9341,rotate=90</li>
      <li>dtparam=bgr=on</li>
      <li>dtparam=reset_pin=25</li>
      <li>dtparam=dc_pin=24</li>
      <li>dtparam=speed=32000000</li>
    </ul>
  </ul>
</li>
