//  The Helixator
//	html5 version
//
//  By Kael Fischer
//    1996-2011
//  kael.fischer@gmail.com
//
//  www interface can be found at:
//	 http://kael.net/helical.htm
//
//  Other versions in:
//  Java, Perl (generates Postscript wheel), Python (uses GD-PIL)
//
//  When I am learning a new suitable language this is the first
//  useful thing I code.  In this case the <canvas> tag is the impetus
//

function Wheel (myCanvas) {
    this.canvas=document.getElementById(myCanvas);
    this.resFill= { 
	G:"#FFFFFF",
	P:"#FFFFFF",
	A:"#FFFFFF",
	V:"#FFFFFF",
	L:"#FFFFFF",
	I:"#FFFFFF",
	M:"#FFFFFF",
	C:"#FFFFFF",
	F:"#FFFFFF",
	Y:"#FFFFFF",
	W:"#FFFFFF",
	H:"#FFFFFF",
	K:"#FF0000",
	R:"#FFFFFF",
	Q:"#FFFFFF",
	N:"#FFFFFF",
	E:"#FFFFFF",
	D:"#FFFFFF",
	S:"#FFFFFF",
	T:"#FFFFFF",}
    this.fgFill= { 
	G:"#000000",
	P:"#000000",
	A:"#000000",
	V:"#000000",
	L:"#000000",
	I:"#000000",
	M:"#000000",
	C:"#000000",
	F:"#000000",
	Y:"#000000",
	W:"#000000",
	H:"#000000",
	K:"#00FF00",
	R:"#000000",
	Q:"#000000",
	N:"#000000",
	E:"#000000",
	D:"#000000",
	S:"#000000",
	T:"#000000",}

    this.direction=0; // 0=into page; 1 out of page
    this.axisStyle=0; // 0 vector; 2 spot ;3 none
    this.sequence="RMKQLEDKVEELLSKNYH";
    
    this.cx=this.canvas.width/2;
    this.cy=this.canvas.height/2;
    this.sm_circ=this.canvas.width/100*5;
    this.link=this.canvas.width/100*3;
    this.radius=this.canvas.width/100*35;
    this.vectorSize=this.canvas.width/100*2;
}

Wheel.prototype.wipe = function () {
    var c=this.canvas.getContext('2d');
    c.stroke();
    c.beginPath();
    c.fillStyle="#FFFFFF";
    c.fillRect(0,0,this.canvas.width,this.canvas.height);
    c.stroke();
}

Wheel.prototype.setColors = function (colorSpecs){
    //colorspecs is an array of textarea-like elements
    //with color and backgroundColor CSS attributes
    //to apply the the resudues in the element
    for (r in this.resFill){
	this.resFill[r]="#FFFFFF";
	this.fgFill[r]="#000000";
    }

    for (i=0;i<colorSpecs.length;i++){
	var s=$(colorSpecs[i]);
	var letters = s.val().split('');
	for (j=0;j<letters.length;j++){
	    this.fgFill[letters[j]]=s.css('color');
	    this.resFill[letters[j]]=s.css('backgroundColor');
	}
    }
}




Wheel.prototype.draw = function (){
    this.wipe();
    if (this.direction == 0){
	step = '1.745';   //That's 100 degrees in radians
    } else {
	step = '-1.745';   
    }
    var offset_angle=0;
    var c=this.canvas.getContext('2d');
    c.font="14pt sans-serif;"
    c.beginPath();
    c.fillStyle="#000000";
    if (this.axisStyle==0) {  //draw the axis
	if (this.direction == 1) {  			// arrow head
	    c.moveTo( this.cx+this.vectorSize/3,this.cy);
	    c.arc(this.cx,this.cy,this.vectorSize/3,0,6.5);
	    c.fill();
	    c.moveTo( this.cx+this.vectorSize,this.cy);
	    c.arc(this.cx,this.cy,this.vectorSize,0,6.5);
	} else {  					// arrow tail
	    c.moveTo( this.cx+this.vectorSize,this.cy);
	    c.arc(this.cx,this.cy,this.vectorSize,0,6.5);
	    c.moveTo(this.cx+this.vectorSize,this.cy);
	    c.lineTo(this.cx-this.vectorSize ,this.cy);
	    c.moveTo(this.cx,this.cy+this.vectorSize);
	    c.lineTo(this.cx ,this.cy-this.vectorSize);
	}
    } else if (this.axisStyle==2) {
	c.arc(this.cx,this.cy,this.vectorSize/3,0,6.5);
	c.fill();
    }
    c.stroke();
    //draw wheel
    var residues = this.sequence.split('');
    for (i=0; i< residues.length;i++){
	var start_x = this.cx + this.radius * Math.cos(offset_angle + step * i);
	var end_x = this.cx + this.radius * Math.cos(offset_angle + step * (i + 1));

	var start_y = this.cy + this.radius * Math.sin(offset_angle + step * i);
	var end_y = this.cy + this.radius *Math. sin(offset_angle + step * (i + 1));

	var link_x = start_x + this.link * Math.cos(offset_angle + step * i);
	var link_y = start_y + this.link * Math.sin(offset_angle + step * i);

	var label_x = link_x + this.sm_circ * Math.cos(offset_angle + step * i);
	var label_y = link_y + this.sm_circ * Math.sin(offset_angle + step * i);

	c.beginPath();
	if (i < residues.length-1 ){  //don't draw a conneting line for last residue
	    c.moveTo(start_x, start_y);
	    c.lineTo(end_x, end_y);
	}
	c.moveTo(start_x, start_y);
	c.lineTo(link_x, link_y);
	c.moveTo(label_x+this.sm_circ,label_y);
	c.stroke();
	
	// now a circle with a letter
	var origFill= c.fillStyle;

	c.fillStyle=this.resFill[residues[i].toUpperCase()];
	
	c.arc(label_x,label_y,this.sm_circ,0,6.5);
	c.fill();
	c.stroke();
	var letterWidth=c.measureText(residues[i]).width
	c.fillStyle=this.fgFill[residues[i].toUpperCase()];
	c.fillText(residues[i],label_x-letterWidth/2,label_y+letterWidth/2);
	c.stroke()
	c.fillStyle=origFill;
	
    }
    
    c.stroke();

}

