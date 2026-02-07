const fs = require('fs');
const path = require('path');

async function checkMainPage() {
    const workspaceDir = '/home/s0u7a/.openclaw/workspace';
    const cookiePath = path.join(workspaceDir, 'note_projects/cookies.json');
    const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf8'));
    const cookieString = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    const userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

    const resp = await fetch('https://note.com/', {
        headers: {
            'Cookie': cookieString,
            'User-Agent': userAgent
        }
    });

    console.log("Status:", resp.status);
    const text = await resp.text();
    if (text.includes('nickname')) {
        console.log("Found 'nickname' in the page. Likely logged in.");
        // Try to find the nickname
        const match = text.match(/"nickname":"(.*?)"/);
        if (match) console.log("Nickname:", match[1]);
    } else {
        console.log("Could not find 'nickname'. Likely NOT logged in.");
        // Log a bit of the body to see what it is
        console.log("Snippet:", text.substring(0, 1000));
    }
}

checkMainPage();
