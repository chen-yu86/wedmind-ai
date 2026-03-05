const timelineDiv=document.getElementById("timeline")

timeline.forEach(item=>{
const div=document.createElement("div")
div.className="timeline-item"
div.innerHTML=item.time+" "+item.step
timelineDiv.appendChild(div)
})

const ctx=document.getElementById("budgetChart")

new Chart(ctx,{
type:"pie",
data:{
labels:Object.keys(budget),
datasets:[{data:Object.values(budget)}]
}
})

const total=Object.values(budget).reduce((a,b)=>a+b,0)
document.getElementById("totalBudget").innerText="婚禮總預算："+total+" 元"

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

function updateProgress(){

const checks=document.querySelectorAll("input[type=checkbox]")

const total=checks.length

const done=[...checks].filter(c=>c.checked).length

const percent=Math.round(done/total*100)

document.getElementById("progressBar").style.width=percent+"%"

document.getElementById("progressText").innerText="完成 "+done+"/"+total

}