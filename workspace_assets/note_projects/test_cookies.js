const fs = require('fs');
const path = require('path');

async function checkCookies() {
    const workspaceDir = '/home/s0u7a/.openclaw/workspace';
    const cookiePath = path.join(workspaceDir, 'note_projects/cookies.json');
    const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf8'));
    const cookieString = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    const userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

    const resp = await fetch('https://note.com/api/v1/notifications', {
        headers: {
            'Cookie': cookieString,
            'User-Agent': userAgent
        }
    });

    console.log("Status:", resp.status);
    const text = await resp.text();
    console.log("Response:", text.substring(0, 500));
}

checkCookies();
