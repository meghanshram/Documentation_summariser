document.addEventListener("DOMContentLoaded", () => {
  // Reference the "Ask" button, question input, and response box
  const askButton = document.getElementById("ask");
  const responseBox = document.getElementById("response");

  // Apply predefined styles for consistent appearance
  const popup = document.body;
  popup.style.backgroundColor = "#f4f4f9"; // Light grey background
  popup.style.color = "#333333"; // Dark grey text
  popup.style.fontFamily = "Arial, sans-serif"; // Clean font

  // Add click listener for the "Ask" button
  askButton.addEventListener("click", async () => {
    const question = document.getElementById("question").value;

    // Get the current tab URL
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;

    // Handle empty questions
    if (!question) {
      responseBox.style.display = "block";
      responseBox.innerText = "Please enter a question.";
      return;
    }

    // Show "Fetching answer..." message
    responseBox.style.display = "block";
    responseBox.innerText = "Fetching answer...";

    // Send the question and URL to the backend
    // try {
    //   const response = await fetch("http://localhost:5000/query-documentation", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({ url, question }),
    //   });

    //   const data = await response.json();
    //   responseBox.innerText = data.response || "No answer found.";
    // } 
    // catch (error) {
    //   console.error("Error:", error);
    //   responseBox.innerText = "Error fetching answer.";
    // }
    fetch("http://localhost:5000/query-documentation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("response").innerHTML = marked.parse(data.response.markdown);
        } else {
            document.getElementById("response").innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        print(error);
        document.getElementById("response").innerText = "An error occurred."+error;
    });
  
    
  });
});
