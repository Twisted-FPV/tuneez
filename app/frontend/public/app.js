const form=document.getElementById('form');
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const fd=new FormData(form);
  const build={
    craft_type:craft_type.value, flight_style:flight_style.value, frame_size:frame_size.value,
    gyro:gyro.value, motor_kv:Number(motor_kv.value||0), battery_cells:Number(battery_cells.value||0),
    symptoms:symptoms.value.split(',').map(s=>s.trim()).filter(Boolean)
  };
  fd.append('build_json', JSON.stringify(build));
  summary.textContent='Analyzing...';
  const res=await fetch('/api/analyze',{method:'POST',body:fd});
  const data=await res.json();
  summary.textContent=data.summary || JSON.stringify(data);
  scores.innerHTML=Object.entries(data.scores||{}).map(([k,v])=>`<span class="score">${k}: ${Number(v).toFixed(1)}</span>`).join('');
  findings.innerHTML=(data.findings||[]).map(f=>`<div class="finding"><b>${f.title}</b> (${f.severity}, ${Math.round(f.confidence*100)}%)<p>${f.why}</p><p><b>Recommendation:</b> ${f.recommendation}</p></div>`).join('');
  cli.textContent=data.cli || '';
});
serial.onclick=async()=>{const res=await fetch('/api/fc-mode',{method:'POST'});serialOut.textContent=JSON.stringify(await res.json(),null,2);}
