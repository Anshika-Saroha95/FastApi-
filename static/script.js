const patientForm = document.getElementById("patient-form");
const patientTableBody = document.getElementById("patient-table-body");
const patientSearch = document.getElementById("patient-search");

const totalPatientsElement = document.getElementById("total-patients");
const newPatientsElement = document.getElementById("new-patients");
const patientCountLabel = document.getElementById("patient-count-label");
const formMessage = document.getElementById("form-message");

let allPatients = {};
let patientChart = null;


// Format patient names into initials
function getInitials(name) {
    return (name || "Patient")
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map(part => part.charAt(0).toUpperCase())
        .join("");
}


// Convert object values into an array
function getPatientEntries() {
    return Object.entries(allPatients);
}


// Load patient data from FastAPI
async function loadPatients() {
    try {
        const response = await fetch("/view");

        if (!response.ok) {
            throw new Error("Could not load patient records.");
        }

        allPatients = await response.json();

        renderPatients(patientSearch.value);
        updateStatistics();
        updatePatientChart();

    } catch (error) {
        console.error("Error loading patients:", error);

        patientTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-message">
                    Unable to load patient records. Please refresh the page.
                </td>
            </tr>
        `;
    }
}


// Display patients and filter the results
function renderPatients(searchTerm = "") {
    patientTableBody.replaceChildren();

    const term = searchTerm.trim().toLowerCase();

    const filteredPatients = getPatientEntries().filter(
        ([patientId, patient]) => {
            const name = String(patient.name || "").toLowerCase();
            const id = String(patientId).toLowerCase();

            return name.includes(term) || id.includes(term);
        }
    );

    if (filteredPatients.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 6;
        cell.className = "empty-message";
        cell.textContent = term
            ? "No patients match your search."
            : "No patient records found.";

        row.appendChild(cell);
        patientTableBody.appendChild(row);

        patientCountLabel.textContent = "Showing 0 patients";
        return;
    }

    for (const [patientId, patient] of filteredPatients) {
        const row = document.createElement("tr");

        // Patient name and avatar
        const nameCell = document.createElement("td");
        const nameContainer = document.createElement("div");
        const avatar = document.createElement("div");
        const name = document.createElement("strong");

        nameContainer.className = "patient-name";
        avatar.className = "patient-avatar";
        avatar.textContent = getInitials(patient.name);
        name.textContent = patient.name || "Unnamed patient";

        nameContainer.append(avatar, name);
        nameCell.appendChild(nameContainer);

        // Patient ID
        const idCell = document.createElement("td");
        idCell.textContent = patientId;

        // Age
        const ageCell = document.createElement("td");
        ageCell.textContent = patient.age ?? "—";

        // Gender
        const genderCell = document.createElement("td");
        const genderBadge = document.createElement("span");

        genderBadge.className = "gender-badge";

        if (String(patient.gender).toLowerCase() === "female") {
            genderBadge.classList.add("female");
        }

        genderBadge.textContent = patient.gender || "—";
        genderCell.appendChild(genderBadge);

        // BMI
        const bmiCell = document.createElement("td");
        bmiCell.textContent =
            patient.bmi !== undefined && patient.bmi !== null
                ? patient.bmi
                : "—";

        // Actions
        const actionsCell = document.createElement("td");
        const actions = document.createElement("div");
        const deleteButton = document.createElement("button");

        actions.className = "action-buttons";
        deleteButton.className = "action-button delete-button";
        deleteButton.type = "button";
        deleteButton.textContent = "Delete";
        deleteButton.setAttribute(
            "aria-label",
            `Delete patient ${patient.name || patientId}`
        );

        deleteButton.addEventListener("click", () => {
            deletePatient(patientId, patient.name);
        });

        actions.appendChild(deleteButton);
        actionsCell.appendChild(actions);

        row.append(
            nameCell,
            idCell,
            ageCell,
            genderCell,
            bmiCell,
            actionsCell
        );

        patientTableBody.appendChild(row);
    }

    patientCountLabel.textContent =
        `Showing ${filteredPatients.length} of ${getPatientEntries().length} patients`;
}


// Update dashboard statistics
function updateStatistics() {
    const patients = getPatientEntries();

    totalPatientsElement.textContent = patients.length;

    // Accurate "new today" statistics require a registration timestamp.
    // Until the backend stores one, display a dash rather than guess.
    newPatientsElement.textContent = "—";
}


// Update chart using the current patient records
function updatePatientChart() {
    const canvas = document.getElementById("patient-chart");

    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    const patients = getPatientEntries().map(([, patient]) => patient);

    const maleCount = patients.filter(
        patient => String(patient.gender).toLowerCase() === "male"
    ).length;

    const femaleCount = patients.filter(
        patient => String(patient.gender).toLowerCase() === "female"
    ).length;

    const otherCount = patients.filter(
        patient => String(patient.gender).toLowerCase() === "others"
    ).length;

    if (patientChart) {
        patientChart.destroy();
    }

    patientChart = new Chart(canvas, {
        type: "bar",

        data: {
            labels: ["Male", "Female", "Others"],

            datasets: [{
                label: "Number of Patients",
                data: [maleCount, femaleCount, otherCount],
                backgroundColor: ["#2875df", "#f05c69", "#8b5cf6"],
                borderRadius: 6,
                maxBarThickness: 55
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    display: false
                }
            },

            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                },

                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}


// Delete a patient through the FastAPI endpoint
async function deletePatient(patientId, patientName) {
    const confirmed = confirm(
        `Are you sure you want to delete ${patientName || patientId}?`
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `/delete/${encodeURIComponent(patientId)}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof result.detail === "string"
                    ? result.detail
                    : JSON.stringify(result.detail || result)
            );
        }

        alert(result.message || "Patient deleted successfully!");

        await loadPatients();

    } catch (error) {
        alert("Error deleting patient: " + error.message);
        console.error("Delete error:", error);
    }
}


// Add a patient through the FastAPI endpoint
patientForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const patientData = {
        id: document.getElementById("patient-id").value.trim(),
        name: document.getElementById("name").value.trim(),
        city: document.getElementById("city").value.trim(),
        age: Number(document.getElementById("age").value),
        gender: document.getElementById("gender").value,
        height: Number(document.getElementById("height").value),
        weight: Number(document.getElementById("weight").value)
    };

    try {
        const response = await fetch("/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patientData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof result.detail === "string"
                    ? result.detail
                    : JSON.stringify(result.detail || result)
            );
        }

        formMessage.textContent =
            result.message || "Patient added successfully!";

        formMessage.style.color = "#059669";

        patientForm.reset();

        await loadPatients();

    } catch (error) {
        formMessage.textContent = "Error: " + error.message;
        formMessage.style.color = "#dc2626";

        console.error("Create patient error:", error);
    }
});


// Search as the user types
patientSearch.addEventListener("input", function () {
    renderPatients(this.value);
});


// Buttons that scroll to the Add Patient form
[
    "open-patient-form",
    "banner-add-patient",
    "table-add-patient"
].forEach(buttonId => {
    const button = document.getElementById(buttonId);

    button.addEventListener("click", () => {
        document.getElementById("add-patient-section")
            .scrollIntoView({ behavior: "smooth" });

        document.getElementById("patient-id").focus();
    });
});


// Set today's date
document.getElementById("today-date").textContent =
    new Date().toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric"
    });


// Activate Lucide icons when the library is available
if (window.lucide) {
    window.lucide.createIcons();
}


// Load the dashboard
loadPatients();

