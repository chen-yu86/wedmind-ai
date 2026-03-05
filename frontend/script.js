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