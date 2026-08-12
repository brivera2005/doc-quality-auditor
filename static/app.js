const $ = (id) => document.getElementById(id);

async function loadSample(name) {
 const res = await fetch(`/api/samples/${name}`);
 const data = await res.json();
 $("noteText").value = data.content;
}

async function runAudit() {
 const btn = $("auditBtn");
 const note = $("noteText").value.trim();
 if (note.length < 20) {
 $("gapReport").innerHTML = '<p class="placeholder">Note must be at least 20 characters.</p>';
 return;
 }
 btn.disabled = true;
 btn.textContent = "Auditing…";
 try {
 const res = await fetch("/api/audit", {
 method: "POST",
 headers: { "Content-Type": "application/json" },
 body: JSON.stringify({
 encounter_note: note,
 encounter_type: $("encounterType").value,
 }),
 });
 if (!res.ok) throw new Error(await res.text());
 renderReport(await res.json());
 } catch (err) {
 $("gapReport").innerHTML = `<p class="placeholder">Error: ${err.message}</p>`;
 } finally {
 btn.disabled = false;
 btn.textContent = "Run audit";
 }
}

function renderReport(data) {
 const s = data.summary;
 $("compliance").textContent = `${s.compliance_pct}%`;
 $("passed").textContent = s.passed;
 $("gaps").textContent = s.gaps;

 let html = "";
 if (data.gaps.length) {
 html += data.gaps
 .map(
 (g) => `
 <article class="gap-card">
 <div class="mid">${g.measure_id} · ${g.category}</div>
 <h3>${g.measure_name}</h3>
 <p class="finding">${g.finding}</p>
 <div class="addendum"><strong>Suggested addendum</strong>${g.suggested_addendum || ""}</div>
 </article>`
 )
 .join("");
 } else {
 html = '<p class="placeholder">No documentation gaps detected for this encounter type.</p>';
 }

 if (data.passed.length) {
 html += `<div class="pass-section"><h4>Passed measures (${data.passed.length})</h4><ul class="pass-list">`;
 html += data.passed
 .map((p) => `<li>${p.measure_id} - ${p.measure_name}<span>${p.finding}</span></li>`)
 .join("");
 html += "</ul></div>";
 }

 $("gapReport").innerHTML = html;
}

$("auditBtn").addEventListener("click", runAudit);
document.querySelectorAll("[data-sample]").forEach((btn) => {
 btn.addEventListener("click", async () => {
 await loadSample(btn.dataset.sample);
 runAudit();
 });
});

loadSample("encounter-note-gaps").then(() => runAudit());
