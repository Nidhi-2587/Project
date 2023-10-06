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

function firstBotMessage() {
    let firstMessage = "How can I help you?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

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

function displayMessage(message) {
    const chatbox = document.getElementById("chatbox");
    const messageElement = document.createElement("div");
    messageElement.className = "message";

    messageElement.innerHTML = `<p class="botText"><span>${message}</span></p>`;

    chatbox.appendChild(messageElement);

    document.getElementById("chat-bar-bottom").scrollIntoView(true);
    
}

document.getElementById("textInput").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

document.querySelector(".fa-send").addEventListener("click", function () {
    sendMessage();
});

document.addEventListener("DOMContentLoaded", function () {
    sendMessage();
});

document.getElementById("chat-button").addEventListener("click", function () {
    document.getElementById("chat-icon").style.color = "green";
    
    setTimeout(function () {
        document.getElementById("chat-icon").style.color = "#fff"; // Reset to the original color
    }, 1000); // Change back to the original color after 1 second (adjust the delay as needed)
});

