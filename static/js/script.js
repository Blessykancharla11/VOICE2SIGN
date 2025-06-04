// JavaScript to handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const textInputField = document.getElementById('textInputField');
    const submitText = document.getElementById('submitText');
    const startVoice = document.getElementById('startVoice');
    const voiceStatus = document.getElementById('voiceStatus');
    const resultDiv = document.getElementById('result');
  
    const textInputArea = document.getElementById('textInputArea');
    const voiceInputArea = document.getElementById('voiceInputArea');
  
    // Show input based on selected type
    const inputTypeRadios = document.getElementsByName('inputType');
    inputTypeRadios.forEach(radio => {
      radio.addEventListener('change', () => {
        if (document.getElementById('textInput').checked) {
          textInputArea.style.display = 'block';
          voiceInputArea.style.display = 'none';
        } else {
          textInputArea.style.display = 'none';
          voiceInputArea.style.display = 'block';
        }
      });
    });
  
    // Handle text submission
    submitText.addEventListener('click', async () => {
      const textInput = textInputField.value.trim();
      if (textInput) {
        const response = await fetch('/find-keypoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ input: textInput, type: 'text' }),
        });
        const data = await response.json();
        resultDiv.innerHTML = `<p>Matches found: ${JSON.stringify(data.matches)}</p>`;
      }
    });
  
    // Handle voice input
    startVoice.addEventListener('click', () => {
      if (!('webkitSpeechRecognition' in window)) {
        alert('Speech Recognition API not supported');
        return;
      }
  
      const recognition = new webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.start();
  
      recognition.onstart = () => {
        voiceStatus.textContent = 'Listening...';
      };
  
      recognition.onresult = async (event) => {
        const voiceInput = event.results[0][0].transcript;
        voiceStatus.textContent = `You said: ${voiceInput}`;
        const response = await fetch('/find-keypoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ input: voiceInput, type: 'voice' }),
        });
        const data = await response.json();
        resultDiv.innerHTML = `<p>Matches found: ${JSON.stringify(data.matches)}</p>`;
      };
  
      recognition.onerror = () => {
        voiceStatus.textContent = 'Error occurred. Please try again.';
      };
    });
  });
  