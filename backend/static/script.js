document.getElementById("generateBtn").addEventListener("click", uploadPDF);

async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");
    const notesBox = document.getElementById("notes");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    notesBox.value = "Generating study notes... Please wait.";

    try {

        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server Error: " + response.status);
        }

        const data = await response.json();

        console.log(data);

        alert(JSON.stringify(data));

        notesBox.value = data.notes;

        

    } catch (error) {

        console.error(error);
        notesBox.value = "Error: " + error.message;

    }

}