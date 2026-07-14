// =========================
// AWS API Gateway URL
// =========================
const API_URL = "https://17srilfx3d.execute-api.us-east-1.amazonaws.com/prod/check";

// =========================
// Analyze Resume
// =========================
async function checkATS() {

    const loading = document.getElementById("loading");
    loading.style.display = "block";

    const file = document.getElementById("resume").files[0];

    if (!file) {
        loading.style.display = "none";
        alert("Please upload a PDF Resume.");
        return;
    }

    const jd = document.getElementById("jd").value.trim();

    if (jd === "") {
        loading.style.display = "none";
        alert("Please enter the Job Description.");
        return;
    }

    const reader = new FileReader();

    reader.onload = async function () {

        try {

            const base64 = reader.result.split(",")[1];

            console.log("Sending request...");
            console.log("Base64 Length:", base64.length);

            const response = await fetch(API_URL, {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    resume: base64,
                    jd: jd
                })

            });

            console.log("HTTP Status:", response.status);

            const data = await response.json();

            console.log("Response:", data);

            loading.style.display = "none";

            if (!response.ok) {

                alert(data.error || "Server Error");

                return;

            }

            const result = data.body ? JSON.parse(data.body) : data;

            showResult(result);

        }

        catch (err) {

            loading.style.display = "none";

            console.error(err);

            alert("Error : " + err.message);

        }

    };

    reader.readAsDataURL(file);

}

// =========================
// Display Result
// =========================
function showResult(result) {

    document.getElementById("score").innerHTML = result.score + "%";

    document.getElementById("progressBar").style.width = result.score + "%";

    const score = document.getElementById("score");

    const status = document.getElementById("status");

    if (result.score >= 80) {

        score.style.color = "green";

        status.innerHTML = "🟢 Excellent Match";

    }

    else if (result.score >= 60) {

        score.style.color = "orange";

        status.innerHTML = "🟡 Good Match";

    }

    else {

        score.style.color = "red";

        status.innerHTML = "🔴 Needs Improvement";

    }

    document.getElementById("analysis").innerHTML = `
        <b>Resume Skills Found:</b> ${result.resumeSkills.length}<br>
        <b>Required Skills:</b> ${result.requiredSkills.length}<br>
        <b>Matched Skills:</b> ${result.matched.length}<br>
        <b>Missing Skills:</b> ${result.missing.length}<br>
        <b>ATS Score:</b> ${result.score}%
    `;

    document.getElementById("matched").innerHTML = "";

    result.matched.forEach(skill => {

        document.getElementById("matched").innerHTML +=
            `<li>✅ ${skill}</li>`;

    });

    document.getElementById("missing").innerHTML = "";

    result.missing.forEach(skill => {

        document.getElementById("missing").innerHTML +=
            `<li>❌ ${skill}</li>`;

    });

    document.getElementById("suggestions").innerHTML = "";

    result.suggestions.forEach(item => {

        document.getElementById("suggestions").innerHTML +=
            `<li>${item}</li>`;

    });

}

// Make functions available to HTML onclick
window.checkATS = checkATS;
window.showResult = showResult;
