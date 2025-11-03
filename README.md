# Texthooker proxy
This is a very simple utility tool that listens on websocket connections and forwards them to
renji's [texthooker-ui](https://renji-xd.github.io/texthooker-ui/) website (or any other arbitrary websocket client).

# Installation
You need Python for this.
```
pip install texthooker_proxy
```

# Usage
By default, it attempts to connect to the default `localhost:6677` address.
```bash
texthooker_proxy
```
You can also supply custom parameters:
```bash
texthooker_proxy --host localhost --port 6678
```

# Scripts for websites
The following scripts are used to hook to VNs on the web. For each of them, you must open the browser
console and paste the corresponding script. Usually, the common keybind is `Ctrl + Shift + I`, and then
click on "Console" and you can paste the code.

## Nostalgic Visual Novels on-line
For [tss.asenheim.org](https://tss.asenheim.org/):
```js
// Open WebSocket connection to your proxy server. 
// This address should match the proxy's
const socket = new WebSocket('ws://localhost:6677');

// When the connection is open, mark this client as the data source
socket.onopen = () => {
    console.log('Connected to WebSocket server.');
    socket.send('notrenji');
    sendTextContainerContent(); // Send initial content
};

// All dialogue is in #text_container
function sendTextContainerContent() {
    const textContainer = document.getElementById('text_container');
    if (textContainer && socket.readyState === WebSocket.OPEN) {
        socket.send(textContainer.textContent);
        console.log('Sent:', textContainer.textContent);
    }
}

// Watch for changes
const observer = new MutationObserver(sendTextContainerContent);
const textContainer = document.getElementById('text_container');
if (textContainer) {
    observer.observe(textContainer, {
        childList: true,
        subtree: true,
        characterData: true
    });
}

socket.onmessage = (event) => {
    console.log('Received:', event.data);
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

socket.onclose = () => {
    console.log('WebSocket connection closed');
};
```