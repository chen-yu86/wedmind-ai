let budgetChart = null

document.addEventListener("DOMContentLoaded",()=>{

renderTimeline()
renderBudget()
renderChecklist()

const slider=document.getElementById("venueSlider")

if(slider){

slider.addEventListener("input",function(){

budget["餐廳"]=parseInt(this.value)

renderBudget()

})

}

})

function renderTimeline(){

const timelineDiv=document.getElementById("timeline")

timelineDiv.innerHTML=""

timeline.forEach((item,i)=>{

setTimeout(()=>{

const div=document.createElement("div")

div.className="timeline-item"

div.innerHTML="<b>"+item.time+"</b> - "+item.step

timelineDiv.appendChild(div)

},i*200)

})

}

function renderBudget(){

const ctx=document.getElementById("budgetChart")

const labels=Object.keys(budget)

const values=Object.values(budget)

const total=values.reduce((a,b)=>a+b,0)

document.getElementById("totalBudget").innerText=
"婚禮總預算："+total.toLocaleString()+" 元"

if(budgetChart){
budgetChart.destroy()
}

budgetChart=new Chart(ctx,{

type:"pie",

data:{

labels:labels,

datasets:[{

data:values,

backgroundColor:[
"#c8a96a",
"#d9b97a",
"#e5c892",
"#f0d7a9",
"#f5e2bd",
"#e0c08a",
"#c4a66f"
]

}]

},

options:{

responsive:true,

animation:{
duration:800
}

}

})

}

function renderChecklist(){

const table=document.getElementById("checklist")

table.innerHTML=""

checklist.forEach(item=>{

const tr=document.createElement("tr")

const td1=document.createElement("td")
const td2=document.createElement("td")

const checkbox=document.createElement("input")

checkbox.type="checkbox"

checkbox.onchange=updateProgress

td1.appendChild(checkbox)

td2.innerText=item

tr.appendChild(td1)
tr.appendChild(td2)

table.appendChild(tr)

})

}

function updateProgress(){

const checks=document.querySelectorAll("input[type=checkbox]")

const total=checks.length

const done=[...checks].filter(c=>c.checked).length

const percent=Math.round(done/total*100)

document.getElementById("progressBar").style.width=
percent+"%"

document.getElementById("progressText").innerText=
"完成 "+done+"/"+total+" ("+percent+"%)"

}

function showSection(section){

document.getElementById("timelineSection").style.display="none"
document.getElementById("budgetSection").style.display="none"
document.getElementById("checklistSection").style.display="none"

if(section==="timeline"){
document.getElementById("timelineSection").style.display="block"
}

if(section==="budget"){
document.getElementById("budgetSection").style.display="block"
}

if(section==="checklist"){
document.getElementById("checklistSection").style.display="block"
}

}

function generateAdvice(){

const budgetValue=
parseInt(document.getElementById("budgetInput").value)

if(!budgetValue){

document.getElementById("aiResult").innerText=
"請輸入預算"

return

}

let advice=""

if(budgetValue<500000){

advice="建議小型婚禮（50~80人）"

}

else if(budgetValue<800000){

advice="建議中型婚禮（100~150人）"

}

else{

advice="建議大型婚禮（200人以上）"

}

const venue=Math.round(budgetValue*0.4)

const photo=Math.round(budgetValue*0.1)

const dress=Math.round(budgetValue*0.1)

document.getElementById("aiResult").innerHTML=

`
${advice}<br>

餐廳：約 ${venue.toLocaleString()} 元<br>

婚紗：約 ${dress.toLocaleString()} 元<br>

攝影：約 ${photo.toLocaleString()} 元
`

}