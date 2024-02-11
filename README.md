# PiPod_Zero2W
<p>This project started as a clone of https://github.com/BramRausch/PiPod</p>
<p>His great write-up can be found at: https://hackaday.io/project/26157-pipod</p>
<H3>Motivation</H3>
<p>I created this version to:</p>
<ul><li>Change from the <b>Raspberry Pi Zero</b> to the <b>Pi Zero 2 W</b>.</li>
<li>To document all of the steps necessary to create the PiPod from scratch, starting with a brand new Pi Zero 2 W.</li></ul>
<H3>Benefits</H3>
<ul>
  <li>The <b>Pi Zero 2 W</b> has built-in wifi, which makes it easy to install software and updates.</li>
  <li>Easy to transfer music files, via SFTP over wifi, from a laptop to the PiPod (using WinSCP, for example.)</li>
</ul>
<H3>Hardware changes</H3>
<ul>
  <li>Increase R6 to 3.75 kohm to reduce the battery charging current to 325 mA. This is a 0.28C charge rate (instead of 1C charging) which helps to increase the battery's life.</li>
  <li>Increase R9 to 4.7 kohm to reduce the brightness of the green LED</li>
</ul>
<H3>Structural Software Changes</H3>
<ul>
  <li>Instead of using Retrogame to link the UI buttons to the pygame event que, I use a callback function (triggered by the GPIO change) that directly posts an event to the pygame event que. (See device.py)</li>
  <li>Instead of using the pygame.display.update() method to flush the frame buffer to the LCD at /dev/fb1, it is now done "manually." (See the refresh() method in display.py) This allows you to simultaneously have the Pi 2 W HDMI output connected to a large monitor, while still running the PiPod software updating its small LCD.</li>
</ul>
<H3>Minor Feature Additions</H3>
<ul>
  <li>Added the ability to pull the "song title" and "artist name" from the MP3 filename. Can still pull this metadata from the file if desired; set "UseMeta = True" in playback.py.</li>
  <li>Added an audio equalizer, with the ability to turn it on and off.</li>
</ul>
<H3>Bug Fixes</H3>
<ul>
  <li>When using the file metadata, if an MP3 file had an empty TITLE, ARTIST, and/or ALBUM field, the file would not get registered into info.csv. Now: "Not Sure" is now written into those fields.</li>
  <li>When trying to select a Track, or Artist/Album from the list of Tracks/Artists/Albums, if you used the Right Arrow key, it would fail and stop the application. Now: Fixed.</li>
</ul>
<H3>Known Bugs</H3>
<ul>
  <li>Selecting "Update library" will do so, but then stops the application. Desired: Return to the "Settings" screen.</li>
</ul>
<H3>Feature Todo List</H3>
<ul>
  <li>Make it easier to scroll a long list of song title (or artists, or album titles).</li>
  <li>Be able to set a play mode, such as:
    <ul>
      <li>Normal (sequential playback of whatever was selected: titles/artists/albums)</li>
      <li>Repeat 1 Song(repeat whatever song is playing)</li>
      <li>Shuffle (random play of whatever is selected: titles/artists/albums)</li>
    </ul>
  </li>
  <li>During playback of a song, enter a song-list "subroutine" (and then return to whatever mode you were in) such as:
    <ul>
      <li>Play whatever album this song is from.</li>
      <li>Play all other songs by this artist.</li>
    </ul>
  </li>
  <li>Ability to delete a music file.</li>
  <li>Add an interface to adjust the audio equalizer.</li>
</ul>

<H2>Hardware Parts</H2>
<p>You will need to purchse a bare PCB from https://www.pcbway.com/project/shareproject/PiPod___Raspberry_pi_Zero_portable_music_player.html</p>
<p>Populate it with components as described in the original PiPod project. Some sources for critical components are listed below for convenience:</p>
<ul>
  <li>The Pi Zero 2 W is a direct drop-in replacement for the PiPod's original Pi Zero.</li>
  <li>One source for the 2.2" LCD (Tianma TM022HDH26 that has the ILI9340C/ILI9341 driver IC) is Adafruit, item #1480 ($25).</li>
  <ul>
    <li>Look for the description "2.2 inch TFT LCD 240x320 ILI9341" on eBay</li>
    <li>I purchased the proper display from both "ecdiystore" ($21) and "satisfyelectronics" ($18)</li>
    <li>(Or contact me -- I have extras.)</li>
  </ul>
  <li>The LiPo 1200mAh battery measures 34mm x 62mm x 5mm / 1.3" x 2.4" x 0.2". One source is Adafruit #258.</li>
  <li>The headphone jack is Digikey part CP-SJ2-3573A2-SMT-CT-ND</li>
  <li>The SMPS inductor (L1) is Digikey part 732-2617-1-ND</li>
  <li>The 40-pin connector for the Pi Zero 2 W is Digikey part 609-2231-ND</li>
  <li>The sliding power switch is Digikey part EG1903-ND</li>
  <li>The small USB connector is Digikey part 609-4616-1-ND</li>
  <li>The side-mount pushbutton switches are Digikey part EG4388CT-ND</li>
  <li>The red and green LEDs are Digikey part 1830-1082-1-ND and 1830-1079-1-ND, respectively</li>
</ul>

<H2>Instructions</H2>
<ul><li>Download the OS file "2023-12-05-raspios-bookworm-arm64.img.xz"</li>
<li>Using rufus-3.22.exe (or similar), burn the image to a 128GB micro-SD card.</li>
<li>Assuming you have a fully-assembled PiPod hardware: Connect an HDMI monitor to the Pi Zero 2 W. Also connect a USB expander hub such as the SmartQ
H302S to the Pi Zero usb connector. Connect a USB keyboard and mouse to the hub.</li>
<li>Apply power to the USB connector at the bottom of the PiPod.</li>
<li>Power-up the Pi Zero and go through the configuration screens. Create the user "pi" with a password of your choosing. Make sure wifi is enabled and connected to a network. Reboot.</li>
<li>Type sudo nano /boot/config.txt and make the following changes:
  <ul>
    <li>un-comment dtparam=spi=on (to turn on the SPI port)</li>
    <li>comment-out the "dtparam=audio=on" line</li>
    <li>add a line: dtoverlay=hifiberry-dac</li>
    <li>un-comment dtparam=i2c_arm=on</li>
    <li>If you are going to SSH music files into the PiPod, uncomment the SSH line.</li>
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
<li>sudo reboot now</li>
<li>Verify that the new frame buffer has been created:
  <ul><li>cd to /dev, do ls and verify that there is a /dev/fb1 entry.</li></ul>
</li>
<li>Type the following and verify that snow appears on the PiPod LCD screen:
  <ul><li>while true; do sudo cat /dev/urandom > /dev/fb1; sleep .5; done</li></ul>
</li>
<li>Enter the following lines to install the required packages:
  <ul>
    <li>sudo apt install python3-pygame</li>
    <li>sudo apt install git</li>
    <li>sudo apt install python3-vlc</li>
    <li>sudo apt install python3-alsaaudio</li>
    <li>sudo apt install python3-taglib</li>
  </ul>
</li>
<li>sudo reboot now</li>
<li>cd ~ then type: git clone https://github.com/delhatch/PiPod_Zero2W.git</li>
<li>Verify that the audio is working. Plug headphones into the PiPod and type:
  <ul>
    <li>speaker-test -c2</li>
    <li>If audio is not heard, you may need to go the GUI, right-click on the speaker icon (upper right) and change to the line "snd_rpi_hifiberry_dac"</li>
  </ul>
</li>
<li>Create the directory ~/Music</li>
<li>Move your music files into this Music directory. You can do this two ways:
  <ul>
    <li>Insert a USB Flash stick into the USB hub, and cp the files over.</li>
    <li>Type "ifconfig" (no quotes) and note the IP address. Use the application WinSCP, and use the SFTP protocol, to copy media files from a Windows computer to the PiPod.</li>
  </ul>
</li>
<li>You should now be able to launch the PiPod software, with everything working.
  <ul>
    <li>cd into the directory ~/PiPod_Zero2W/Sofware</li>
    <li>Type: python3 main.py</li>
  </ul>
</li>
</ul>
