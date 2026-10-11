const $=s=>document.querySelector(s);
async function cargar(){
 const est=await fetch("/api/estaciones").then(r=>r.json());
 for(const id of ["#origen","#destino"]){
   $(id).innerHTML=est.map(x=>`<option>${x.nombre}</option>`).join("");
 }
 $("#destino").selectedIndex=Math.min(8,est.length-1);
 const bc=await fetch("/api/conocimiento").then(r=>r.json());
 $("#numEst").textContent=bc.estaciones; $("#numCon").textContent=bc.conexiones.length;
}
$("#swap").onclick=()=>{let a=$("#origen").value;$("#origen").value=$("#destino").value;$("#destino").value=a}
$("#buscar").onclick=async()=>{
 $("#buscar").textContent="Calculando...";
 const res=await fetch("/api/ruta",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({origen:$("#origen").value,destino:$("#destino").value})});
 const d=await res.json(); $("#buscar").textContent="Calcular mejor ruta";
 if(!res.ok){alert(d.error);return}
 $("#costo").textContent=`Costo: ${d.costo_total}`;
 $("#ruta").classList.remove("empty");
 $("#ruta").innerHTML=d.ruta.map((x,i)=>`${i?'<b>→</b>':''}<span>${x}</span>`).join("");
 $("#tramos").innerHTML=d.detalles.map((x,i)=>`<div class="leg"><b>Tramo ${i+1}:</b> ${x.desde} → ${x.hasta} · ${x.corredor} · costo ${x.costo}</div>`).join("");
 $("#proceso").innerHTML=d.exploracion.map(x=>`<tr><td>${x.paso}</td><td><b>${x.estacion}</b></td><td>${x.g}</td><td>${x.h}</td><td>${x.f}</td><td>${x.regla}</td></tr>`).join("");
}
cargar();