const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
const chatbotToggler = document.querySelector(".chatbot-toggler");
const chatbotCloseBtn = document.querySelector(".close-btn");


let userMessage;
let API_KEY = "";
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
  // Create a chat <> element with passed message and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent =
    className === "outgoing"
      ? `<p></p>`
      : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("p").textContent = message;
  return chatLi;
};


const createAudioElement = (message, className) => {
  // Create a chat <> element  with passed audio and className
  const chatLi = document.createElement("li");
  chatLi.classList.add("chat", className);
  let chatContent =
    className === "outgoing"
      ? '<div></div>'
      : `<span class="material-symbols-outlined">smart_toy</span><div></div>`;
  chatLi.innerHTML = chatContent;
  chatLi.querySelector("div").innerHTML = message;
  return chatLi;
}


const generateResponse = (incomingChatLi) => {
  // Generate a random response from the bot
  const API_URL = " http://127.0.0.1:8000/chatbot_response";
  const messageElement = incomingChatLi.querySelector("p");

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      sender: "test_user",
      message: userMessage,
    }),
  };


  // send Post request to API, get response
  fetch(API_URL, requestOptions)
    .then((res) => res.json())
    .then((data) => {
      // Concatenate all messages into one string
      const concatenatedMessage = data
        .map((item) => item.text || item.image)
        .join('\n');

      // Set the messageElement's text content to the concatenated message
      messageElement.textContent = concatenatedMessage;

      console.log(data);
    })
    .catch((err) => {
      messageElement.classList.add("error");
      console.log("err", err);
      messageElement.textContent =
        "Oops! Something went wrong. Please try again later.";
    })
    .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};

const handleChat = () => {
  userMessage = chatInput.value.trim();
  if (!userMessage) return;
  chatInput.value = "";
  chatInput.style.height = inputInitHeight + "px";

  // Append the user's message to the chatbox
  chatbox.appendChild(createChatLi(userMessage, "outgoing"));
  chatbox.scrollTo(0, chatbox.scrollHeight);

  setTimeout(() => {
    // Display "Typing..." message while waiting for the response
    const incomingChatLi = createChatLi("Typing...", "incoming");
    chatbox.appendChild(incomingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);
    generateResponse(incomingChatLi);
  }, 600);
};

chatInput.addEventListener("input", () => {
  // Auto resize the textarea
  chatInput.style.height = inputInitHeight + "px";
  chatInput.style.height = chatInput.scrollHeight + "px";
});

// Fix for Shift+Enter key
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleChat();
  }
});


sendChatBtn.addEventListener("click", handleChat);
chatbotCloseBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));


let mediaRecorder;
let audioChunks = [];

// function to start recording audio
const startRecording = () => {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      const audioUrl = URL.createObjectURL(audioBlob);

      // send the audio URL to the fastAPI server
      sendAudio(audioBlob);

      // Display the audio message in the chatbox
      displayAudioMessage(audioUrl, "outgoing");


      //clear recorded audio chunks
      audioChunks = [];


    }
    mediaRecorder.start();

  }).catch
    ((err) => {
      console.log("err", err);
    });
};

// function to stop recording audio
const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
  }
};

// function to send audio data to the FastAPI server
const sendAudio = (audioBlob) => {
  const formData = new FormData();
  const audioFile = new File([audioBlob], "userVoiceInput.wav", { type: "audio/wav" });
  formData.append("audio_file", audioFile);

  const requestOptions = {
    method: "POST",
    body: formData,
  };

  fetch("http://localhost:8000/audio_message", requestOptions)
    .then((res) => res.blob())
    .then((audioBlob) => {
      // Display the response in the chatbox
      const audioUrl = URL.createObjectURL(audioBlob);
      displayAudioMessage(audioUrl, "incoming");
      chatbox.scrollTo(0, chatbox.scrollHeight);
    }
    )
    .catch((err) => {
      console.log("err", err);
      const messageElement = chatbox.querySelector("li.incoming p");
      messageElement.classList.add("error");
      messageElement.textContent =
        "Oops! Something went wrong. Please try again later.";
    });
};

// function to display audio message in the chatbox
const displayAudioMessage = (audioUrl, messageType) => {
  // create an HTML element (e.g audio player) to play the audio
  const audioElement = document.createElement("audio");
  audioElement.src = audioUrl;
  audioElement.type = "audio/mpeg";
  audioElement.controls = true;

  // Append the audio element to the chatbox for playback
  chatbox.appendChild(createAudioElement(audioElement.outerHTML, messageType));

  // Scroll to the bottom of the chatbox
  chatbox.scrollTo(0, chatbox.scrollHeight);
};

// Get reference to the icons
const recordBtn = document.getElementById("record-btn");
const stopBtn = document.getElementById("stop-btn");

// Add click event listeners to the record button
recordBtn.addEventListener("click", () => {
  // Hide the record button
  recordBtn.style.display = "none";
  startRecording();

  // Show the stop button
  stopBtn.style.display = "inline-block";

});

// Add click event listener to the stop button
stopBtn.addEventListener("click", () => {
  // Hide the stop button
  stopBtn.style.display = "none";
  stopRecording();

  // Show the record button
  recordBtn.style.display = "inline-block";
});
