async function generateDocument() {

    const documentType = document.getElementById("documentType").value;
    const firstParty = document.getElementById("firstParty").value;
    const secondParty = document.getElementById("secondParty").value;
    const agreementDate = document.getElementById("agreementDate").value;
    const request = document.getElementById("documentRequest").value;

    const result = document.getElementById("generationResult");

    if (!documentType) {
        result.innerHTML = `
            <div class="result-box">
                ⚠️ Please select a document type.
            </div>
        `;
        return;
    }

    if (!request.trim()) {
        result.innerHTML = `
            <div class="result-box">
                ⚠️ Please enter your document requirements.
            </div>
        `;
        return;
    }

    result.innerHTML = `
        <div class="result-box">
            🤖 Generating your legal document...
        </div>
    `;

    const fullRequest = `
Document Type: ${documentType}

First Party:
${firstParty}

Second Party:
${secondParty}

Agreement Date:
${agreementDate}

Additional Requirements:
${request}
`;

    try {

        const response = await fetch("/generate", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                request: fullRequest
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Generation failed");
        }

        const generatedText =
            data.document ||
            data.result ||
            data.content ||
            data.message ||
            JSON.stringify(data, null, 2);

        result.innerHTML = `
            <div class="result-box">
                <h3>📄 Generated Legal Document</h3>

                <div style="
                    margin-top:15px;
                    padding:20px;
                    background:#111;
                    border:1px solid #333;
                    border-radius:6px;
                    white-space:pre-wrap;
                ">${escapeHtml(generatedText)}</div>

                <button
                    style="margin-top:15px;"
                    onclick="copyDocument()">
                    📋 Copy Document
                </button>
            </div>
        `;

        window.generatedDocument = generatedText;

    } catch (error) {

        result.innerHTML = `
            <div class="result-box">
                ❌ Unable to generate document.

                <br><br>

                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


async function uploadDocument() {

    const fileInput =
        document.getElementById("documentFile");

    const result =
        document.getElementById("uploadResult");

    if (!fileInput.files.length) {

        result.innerHTML = `
            <div class="result-box">
                ⚠️ Please select a document first.
            </div>
        `;

        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("file", file);

    result.innerHTML = `
        <div class="result-box">
            ⏳ Uploading document...
        </div>
    `;

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Upload failed"
            );
        }

        result.innerHTML = `
            <div class="result-box">
                ✅ Document uploaded successfully.

                <br><br>

                ${escapeHtml(
                    data.message ||
                    data.result ||
                    "Document processed successfully."
                )}
            </div>
        `;

    } catch (error) {

        result.innerHTML = `
            <div class="result-box">
                ❌ Upload failed.

                <br><br>

                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


function copyDocument() {

    if (!window.generatedDocument) {
        return;
    }

    navigator.clipboard.writeText(
        window.generatedDocument
    );

    alert("Document copied!");
}


function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}