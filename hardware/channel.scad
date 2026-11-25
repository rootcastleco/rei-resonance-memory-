// REI Resonance Memory: editable single-channel envelope, NOT FOR FABRICATION.
// Units: mm. No validated fastener, holder, latch or enclosure design.
length=67.11; width=12; thickness=0.8; gap=0.715;
base=[125,54,4];
$fn=48;
color("dimgray") cube(base);
color("silver") translate([8,18,4]) cube([12,18,10]);
color("silver") translate([20,21,14]) cube([length,width,thickness]);
// Nominal mass volume shown only as an envelope; actual weight includes hardware.
color("goldenrod") translate([20+length-7,19,14.8]) cube([14,16,19]);
color("steelblue") translate([20+length-7,21,14-gap-2]) cube([14,12,2]);
// Transparent enclosure outline. No claim of containment capacity.
%translate([2,2,4]) cube([121,50,34]);
