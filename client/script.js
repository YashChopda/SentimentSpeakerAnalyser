// Event listener for changes in file type selection
document.getElementById('fileType').addEventListener('change', function() {
    const fileType = this.value;
    const fileInput = document.getElementById('fileInput');
    
    // Enable/disable file input based on selected file type
    fileInput.disabled = fileType === '';
    
    // Set accepted file types for file input based on selected file type
    fileInput.accept = fileType === 'text' ? '.txt' : fileType === 'audio' ? '.mp3' : '';
});

// Function to upload file and initiate analysis
function uploadFile() {
    // Display loading screen while uploading and processing file
    document.getElementById('loadingScreen').style.display = 'flex';
    
    const fileType = document.getElementById('fileType').value;
    const fileInput = document.getElementById('fileInput');
    
    // Validate file type and file selection
    if (!fileType || fileInput.files.length === 0) {
        alert('Please select a file type and file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    // Determine endpoint based on file type: TODO put your backend server url
    const endpoint = fileType === 'text' ? 'http://35.188.74.198:5000/api/text/query' : 'http://35.188.74.198:5000/api/audio/query';

    // Send file to server for analysis
    fetch(endpoint, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Display analysis results
        displayAnalysis(data);
        // Hide loading screen after analysis is complete
        document.getElementById('loadingScreen').style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
}

// Function to display analysis results
function displayAnalysis(data) {
    const analysisOutput = document.getElementById('analysisOutput');
    const speakers = data.response;
    
    // Initialize variables for tab headers and content
    let tabs = '';
    let tabContent = '';

    // Loop through each speaker in the analysis data
    Object.keys(speakers).forEach((speaker, index) => {
        // Set active class for the first tab and tab content
        const activeClass = index === 0 ? 'active' : '';
        const fadeShowClass = index === 0 ? 'show active' : '';

        // Create tab header HTML
        tabs += `<li class="nav-item">
                    <a class="nav-link ${activeClass}" id="tab-${speaker}" data-toggle="tab" href="#content-${speaker}" role="tab">
                        ${speaker.replace('_', ' ')}
                    </a>
                 </li>`;

        // Create tab content HTML
        tabContent += `<div class="tab-pane fade ${fadeShowClass}" id="content-${speaker}" role="tabpanel">
                            <p>${speakers[speaker]}</p>
                        </div>`;
    });

    // Update analysis output HTML with tab headers and content
    analysisOutput.innerHTML = `<ul class="nav nav-tabs" id="analysisTabs" role="tablist">${tabs}</ul>
                                 <div class="tab-content" id="tabContent">${tabContent}</div>`;

    // Activate tabs
    $('#analysisTabs a').on('click', function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
}
