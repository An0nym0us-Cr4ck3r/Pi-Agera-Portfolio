const fs = require('fs');
const path = require('path');

async function debugMainPage() {
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

    const text = await resp.text();
    // Look for JSON-like data in the HTML
    const jsonMatch = text.match(/<script id="__NEXT_DATA__" type="application\/json">(.*?)<\/script>/);
    if (jsonMatch) {
        const data = JSON.parse(jsonMatch[1]);
        fs.writeFileSync('note_projects/debug_data.json', JSON.stringify(data, null, 2));
        console.log("Saved __NEXT_DATA__ to note_projects/debug_data.json");
        if (data.props && data.props.pageProps && data.props.pageProps.user) {
            console.log("User found in __NEXT_DATA__:", data.props.pageProps.user.nickname);
        }
    } else {
        console.log("__NEXT_DATA__ not found.");
    }
}

debugMainPage();
