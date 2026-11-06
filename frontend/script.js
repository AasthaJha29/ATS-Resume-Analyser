async function analyze() {
  const file = document.getElementById("resume").files[0];
  const jd = document.getElementById("jd").value;

  if (!file) {
    alert("Please upload a resume.");
    return;
  }

  if (!jd.trim()) {
    alert("Please enter a job description.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", file);
  formData.append("jd", jd);

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    // Handle backend errors
    if (data.error) {
      document.getElementById("result").innerHTML =
        `<p style="color:red;"><b>Error:</b> ${data.error}</p>`;
      return;
    }

    document.getElementById("result").innerHTML = `
      <h3>ATS Score: ${data.score}%</h3>
      <p><b>Matched:</b> ${(data.matched || []).join(", ")}</p>
      <p><b>Missing:</b> ${(data.missing || []).join(", ")}</p>
    `;
  } catch (err) {
    document.getElementById("result").innerHTML =
      `<p style="color:red;">Server error. Is backend running?</p>`;
  }
}