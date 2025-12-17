<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.2" name="objects" tilewidth="128" tileheight="64" tilecount="6" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" type="Box">
  <image source="../objects/box.png" width="32" height="32"/>
 </tile>
 <tile id="1" type="Button">
  <properties>
   <property name="trigger_type" value="trigger"/>
  </properties>
  <image source="../objects/button.png" width="32" height="32"/>
 </tile>
 <tile id="2" type="Door">
  <properties>
   <property name="trigger_type" value="trigger"/>
  </properties>
  <image source="../objects/door_closed.png" width="32" height="64"/>
 </tile>
 <tile id="3">
  <image source="../objects/heavybox.png" width="64" height="64"/>
 </tile>
 <tile id="4">
  <image source="../objects/platform.png" width="128" height="32"/>
 </tile>
 <tile id="5">
  <image source="../objects/table.png" width="64" height="32"/>
 </tile>
</tileset>
