// background.js

// 创建右键菜单项
chrome.contextMenus.create({
    id: 'convertToMarkdown',
    title: 'Convert to Markdown',
    contexts: ['all']
});

// 监听右键菜单点击事件
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'convertToMarkdown') {
        chrome.storage.sync.get('serviceUrl', (data) => {
            const serviceUrl = data.serviceUrl;
            if (serviceUrl) {
                chrome.scripting.executeScript({
                    target: {tabId: tab.id},
                    function: convertToMarkdown,
                });
            } else {
                alert('Service URL not configured.');
            }
        });
    }
});

function convertToMarkdown() {
    const pageContent = document.documentElement.outerHTML;
    chrome.storage.sync.get('serviceUrl', (data) => {
        const serviceUrl = data.serviceUrl;
        console.log(serviceUrl)
        if (serviceUrl) {
            fetch("https://"+serviceUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: window.location.href })
            })
                .then(response => response.blob()) // 处理响应为 Blob
                .then(blob => {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'page.md';
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    URL.revokeObjectURL(url);
                })
                .catch(error => console.error('Fetch error:', error));
        } else {
            alert('Service URL not configured.');
        }
    });
}
