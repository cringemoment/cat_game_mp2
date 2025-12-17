<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.2" name="wee" tilewidth="64" tileheight="64" tilecount="6" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0">
  <properties>
   <property name="z" value="1"/>
  </properties>
  <image source="../assets/objects/table.png" width="64" height="32"/>
 </tile>
 <tile id="1">
  <image source="../assets/objects/tableindicator.png" width="64" height="32"/>
 </tile>
 <tile id="2" type="Door">
  <image source="../assets/objects/door_closed.png" width="32" height="64"/>
 </tile>
 <tile id="3">
  <image source="../assets/objects/door_open.png" width="32" height="64"/>
 </tile>
 <tile id="4" type="Button">
  <properties>
   <property name="trigger_type" value="trigger"/>
  </properties>
  <image source="../assets/objects/button.png" width="32" height="32"/>
 </tile>
 <tile id="5">
  <image source="../assets/objects/button_pressed.png" width="32" height="32"/>
 </tile>
</tileset>
