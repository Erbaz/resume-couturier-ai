document.getElementById('loginBtn').addEventListener('click', () => {
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        if (chrome.runtime.lastError) {
            console.error("Auth Error:", chrome.runtime.lastError.message);
            document.getElementById('result').textContent = "Error: " + chrome.runtime.lastError.message;
            return;
        }

        console.log("Access Token retrieved:", token);
        document.getElementById('result').textContent = "Access Token: " + token;

        // Note: chrome.identity.getAuthToken returns an Access Token. 
        // To get the Identity/ID token and user info, you can use the access token to fetch from Google APIs
        fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
            headers: { 'Authorization': 'Bearer ' + token }
        })
        .then(response => response.json())
        .then(data => {
            console.log("User Info / Identity Payload:", data);
            document.getElementById('result').textContent += "\n\nUser: " + data.email;
        })
        .catch(err => console.error("Failed to fetch user info:", err));
    });
});
