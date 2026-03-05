let budgetChart

document.addEventListener("DOMContentLoaded",()=>{

renderTimeline()
renderBudget()
renderChecklist()

showSection("timeline")

const slider=document.getElementById("venueSlider")

slider.addEventListener("input",function(){

const value=parseInt(this.value)

budget["餐廳"]=value

document.getElementById("venueValue").innerText=
"餐廳預算："+value.toLocaleString()+" 元"

renderBudget()

})

})


function renderTimeline(){

const engagementDiv=document.getElementById("engagementTimeline")
const weddingDiv=document.getElementById("weddingTimeline")

engagementDiv.innerHTML=""
weddingDiv.innerHTML=""

engagementTimeline.forEach((item,i)=>{

setTimeout(()=>{

const div=document.createElement("div")

div.className="timeline-item"

div.innerHTML=
"<span class='timeline-time'>"+item.time+"</span> - "+item.step

engagementDiv.appendChild(div)

},i*150)

})

weddingTimeline.forEach((item,i)=>{

setTimeout(()=>{

const div=document.createElement("div")

div.className="timeline-item"

div.innerHTML=
"<span class='timeline-time'>"+item.time+"</span> - "+item.step

weddingDiv.appendChild(div)

},i*150)

})

}


function renderBudget(){

const ctx=document.getElementById("budgetChart")

if(budgetChart){
budgetChart.destroy()
}

budgetChart=new Chart(ctx,{
type:"pie",

data:{
labels:Object.keys(budget),

datasets:[{
data:Object.values(budget),

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
}

})

const total=Object.values(budget).reduce((a,b)=>a+b,0)

document.getElementById("totalBudget").innerText=
"婚禮總預算："+total.toLocaleString()+" 元"

}


function renderChecklist(){

const table=document.getElementById("checklist")

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

const budgetInput=document.getElementById("budgetInput").value

if(!budgetInput){

document.getElementById("aiResult").innerHTML="請先輸入預算"

return

}

const total=parseInt(budgetInput)

const venue=total*0.4
const dress=total*0.15
const photo=total*0.1

document.getElementById("aiResult").innerHTML=

"💡 AI 婚禮預算建議<br><br>"+

"餐廳：約 "+venue.toLocaleString()+" 元<br>"+

"婚紗：約 "+dress.toLocaleString()+" 元<br>"+

"攝影：約 "+photo.toLocaleString()+" 元"

}
