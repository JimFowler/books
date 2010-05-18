
/***********************************************
* Drop Down Date select script- by JavaScriptKit.com
* This notice MUST stay intact for use
* Visit JavaScript Kit at http://www.javascriptkit.com/ for this script and more
***********************************************/

var monthtext=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec'];

function populatedropdown(dayfield, monthfield, yearfield){
var today=new Date()
var dayfield=document.getElementById(dayfield)
var monthfield=document.getElementById(monthfield)
var yearfield=document.getElementById(yearfield)
for (var i=0; i<31; i++)
dayfield.options[i]=new Option(i, i+1)
dayfield.options[today.getDate()]=new Option(today.getDate(), today.getDate(), true, true) //select today's day
for (var m=0; m<12; m++)
monthfield.options[m]=new Option(monthtext[m], monthtext[m])
monthfield.options[today.getMonth()]=new Option(monthtext[today.getMonth()], monthtext[today.getMonth()], true, true) //select today's month
var thisyear=today.getFullYear()
for (var y=0; y<20; y++){
yearfield.options[y]=new Option(thisyear, thisyear)
thisyear+=1
}
yearfield.options[0]=new Option(today.getFullYear(), today.getFullYear(), true, true) //select today's year
}


/*
  Add the below form into the <Body> section
<form action="" name="someform">
<select id="daydropdown">
</select> 
<select id="monthdropdown">
</select> 
<select id="yeardropdown">
</select> 
</form>

<script type="text/javascript">

//populatedropdown(id_of_day_select, id_of_month_select, id_of_year_select)
window.onload=function(){
populatedropdown("daydropdown", "monthdropdown", "yeardropdown")
}
</script>

*/


/**--------------------------
//* Validate Date Field script- By JavaScriptKit.com
//* For this script and 100s more, visit http://www.javascriptkit.com
//* This notice must stay intact for usage
---------------------------**/

function checkdate(input){
var validformat=/^\d{2}\/\d{2}\/\d{4}$/ //Basic check for format validity
var returnval=false
if (!validformat.test(input.value))
alert("Invalid Date Format. Please correct and submit again.")
else{ //Detailed check for valid date ranges
var monthfield=input.value.split("/")[0]
var dayfield=input.value.split("/")[1]
var yearfield=input.value.split("/")[2]
var dayobj = new Date(yearfield, monthfield-1, dayfield)
if ((dayobj.getMonth()+1!=monthfield)||(dayobj.getDate()!=dayfield)||(dayobj.getFullYear()!=yearfield))
alert("Invalid Day, Month, or Year range detected. Please correct and submit again.")
else
returnval=true
}
if (returnval==false) input.select()
return returnval
}

/*
<form onSubmit="return checkdate(this.mydate)">
<input type="text" name="mydate" />
<input type="submit" value="submit" /><br />
<b>Valid date format:</b> mm/dd/yyyy<br />
<input type="submit" value="submit" />
</form>
*/