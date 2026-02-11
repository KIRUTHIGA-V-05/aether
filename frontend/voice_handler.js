const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.continuous = false;

function startListening() {
    recognition.start();
    logToConsole("Aether is listening...");
}

recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('commandInput').value = transcript;
    sendCommand();
};

recognition.onerror = (event) => {
    logToConsole("Speech Recognition Error: " + event.error);
};