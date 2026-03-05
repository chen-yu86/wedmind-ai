document.addEventListener("DOMContentLoaded",()=>{

renderTimeline()
renderBudget()
renderChecklist()

initSlider()

})

// ---------------- 婚禮流程 ----------------

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

// ---------------- 預算圖表 ----------------

let chart=null

function renderBudget(){

const ctx=document.getElementById("budgetChart")

if(chart){
chart.destroy()
}

chart=new Chart(ctx,{
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

// ---------------- 準備清單 ----------------

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

// ---------------- 進度條 ----------------

function updateProgress(){

const checks=document.querySelectorAll("input[type=checkbox]")

const total=checks.length

const done=[...checks].filter(c=>c.checked).length

const percent=Math.round(done/total*100)

document.getElementById("progressBar").style.width=percent+"%"

document.getElementById("progressText").innerText=
"完成 "+done+"/"+total+" ("+percent+"%)"

}

// ---------------- 滑動導航 ----------------

function scrollToTimeline(){
document.getElementById("timeline").scrollIntoView({behavior:"smooth"})
}

function scrollToBudget(){
document.getElementById("budgetChart").scrollIntoView({behavior:"smooth"})
}

function scrollToChecklist(){
document.getElementById("checklist").scrollIntoView({behavior:"smooth"})
}

// ---------------- Slider ----------------

function initSlider(){

const slider=document.getElementById("venueSlider")

if(!slider) return

slider.addEventListener("input",function(){

budget["餐廳"]=parseInt(this.value)

renderBudget()

})

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

advice=
"建議小型婚禮（50~80人）"

}

else if(budgetValue<800000){

advice=
"建議中型婚禮（100~150人）"

}

else{

advice=
"建議大型婚禮（200人以上）"

}

const venue=Math.round(budgetValue*0.4)

const photo=Math.round(budgetValue*0.1)

const dress=Math.round(budgetValue*0.1)

document.getElementById("aiResult").innerHTML=

`
AI 建議婚禮規模<br>

餐廳：約 ${venue.toLocaleString()} 元<br>

婚紗：約 ${dress.toLocaleString()} 元<br>

攝影：約 ${photo.toLocaleString()} 元
`

}
