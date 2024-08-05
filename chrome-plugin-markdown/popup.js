document.addEventListener('DOMContentLoaded', () => {
    const serviceUrlInput = document.getElementById('service-url');
    const saveButton = document.getElementById('save');

    chrome.storage.sync.get('serviceUrl', (data) => {
        serviceUrlInput.value = data.serviceUrl || '';
    });

    saveButton.addEventListener('click', () => {
        const serviceUrl = serviceUrlInput.value;
        chrome.storage.sync.set({ serviceUrl }, () => {
            alert('Service URL saved!');
        });
    });
});
