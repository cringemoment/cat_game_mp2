<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.2" name="objects" tilewidth="128" tileheight="80" tilecount="12" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" type="Box">
  <image source="../objects/box.png" width="32" height="32"/>
 </tile>
 <tile id="1" type="Button">
  <properties>
   <property name="trigger_type" value="trigger"/>
  </properties>
  <image source="../objects/red_button.png" width="32" height="32"/>
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
 <tile id="6" type="TrapDoor">
  <image source="../objects/trapdoor_closed.png" width="64" height="32"/>
 </tile>
 <tile id="7" type="ReverseTrapDoor">
  <image source="../objects/trapdoor_open.png" width="64" height="32"/>
 </tile>
 <tile id="10">
  <image source="../objects/tablewithphone.png" width="96" height="64"/>
 </tile>
 <tile id="11" type="ReverseDoor">
  <image source="../objects/door_open.png" width="32" height="64"/>
 </tile>
 <tile id="12">
  <image source="../objects/cargo_boxes/bluecargo.png" width="128" height="80"/>
 </tile>
 <tile id="13">
  <image source="../objects/cargo_boxes/redcargo.png" width="128" height="80"/>
 </tile>
</tileset>
