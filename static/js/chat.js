// Collapsible
var coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

    });
}

function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;
    return time;
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "How can I help you?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

// Function to send a POST request to the server
function sendMessage() {
    const userInput = document.getElementById("textInput").value;
   
    
    if (userInput.trim() === "") {
        return;
    }

    const requestData = {
        message: userInput
    };

    fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.response);



    })
    .catch(error => {
        console.error("Error:", error);
    });

    // Clear the input field
    document.getElementById("textInput").value = "";

    let userHtml = '<p class="userText"><span>' + userInput + '</span></p>';
    
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

// Function to display a user or chatbot message in the chatbox
function displayMessage(message) {
    const chatbox = document.getElementById("chatbox");
    const messageElement = document.createElement("div");
    messageElement.className = "message";

    messageElement.innerHTML = `<p class="botText"><span>${message}</span></p>`;

    chatbox.appendChild(messageElement);

    // Scroll to the bottom of the chatbox to show the latest message
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
    
}

// Event listener for the Enter key
document.getElementById("textInput").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Event listener for the send button
document.querySelector(".fa-send").addEventListener("click", function () {
    sendMessage();
});

// Initial message when the page loads
document.addEventListener("DOMContentLoaded", function () {
    sendMessage();
});

// Event listener for the chat button
document.getElementById("chat-button").addEventListener("click", function () {
    // Change the color of the chat icon when clicked
    document.getElementById("chat-icon").style.color = "green";
    
    // Optionally, you can reset the color after a certain delay
    setTimeout(function () {
        document.getElementById("chat-icon").style.color = "#fff"; // Reset to the original color
    }, 1000); // Change back to the original color after 1 second (adjust the delay as needed)
});

