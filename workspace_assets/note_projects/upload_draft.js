const fs = require('fs');
const path = require('path');

/**
 * Note.com Draft Upload Infrastructure
 * Uses cookies to authenticate and upload a markdown file as a draft.
 */
async function uploadDraft(articleFilePath) {
    const workspaceDir = '/home/s0u7a/.openclaw/workspace';
    const cookiePath = path.join(workspaceDir, 'note_projects/cookies.json');
    
    if (!fs.existsSync(cookiePath)) {
        throw new Error('Cookies file not found at ' + cookiePath);
    }
    if (!fs.existsSync(articleFilePath)) {
        throw new Error('Article file not found at ' + articleFilePath);
    }

    const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf8'));
    let article = fs.readFileSync(articleFilePath, 'utf8').trim();

    // Clean up markdown block if present
    article = article.replace(/^```markdown\n/, '').replace(/\n```$/, '');

    const lines = article.split('\n');
    let title = 'Untitled';
    let contentLines = [];
    let foundTitle = false;

    for (const line of lines) {
        if (!foundTitle && line.startsWith('## ')) {
            title = line.replace('## ', '').trim();
            foundTitle = true;
        } else {
            contentLines.push(line);
        }
    }
    const content = contentLines.join('\n').trim();

    // Simple Markdown to HTML conversion
    let html = content
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/^\* (.+)$/gm, '<li>$1</li>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Paragraph handling
    html = html.split('\n\n').map(p => {
        p = p.trim();
        if (!p) return '';
        if (p.startsWith('<h') || p.startsWith('<li')) return p;
        return `<p>${p.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');

    let cookieMap = new Map();
    cookies.forEach(c => cookieMap.set(c.name, c.value));
    
    const userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

    console.log(`[Note Infrastructure] Initializing session for "${title}"...`);

    // 1. Get XSRF-TOKEN and update session
    const initResp = await fetch('https://note.com/notes/new', {
        headers: { 
            'Cookie': Array.from(cookieMap.entries()).map(([k,v]) => `${k}=${v}`).join('; '),
            'User-Agent': userAgent 
        }
    });
    
    const setCookies = initResp.headers.getSetCookie();
    setCookies.forEach(sc => {
        const parts = sc.split(';')[0].split('=');
        if (parts.length >= 2) {
            cookieMap.set(parts[0].trim(), parts.slice(1).join('=').trim());
        }
    });

    const xsrfToken = cookieMap.get('XSRF-TOKEN') || '';

    // 2. Post Draft
    const postHeaders = {
        'Content-Type': 'application/json',
        'Cookie': Array.from(cookieMap.entries()).map(([k,v]) => `${k}=${v}`).join('; '),
        'User-Agent': userAgent,
        'X-XSRF-TOKEN': xsrfToken ? decodeURIComponent(xsrfToken) : '',
        'Referer': 'https://note.com/notes/new',
        'Origin': 'https://note.com'
    };

    const payload = {
        body: html,
        name: title,
        template_key: null
    };

    console.log(`[Note Infrastructure] Uploading to API...`);
    const resp = await fetch('https://note.com/api/v1/text_notes', {
        method: 'POST',
        headers: postHeaders,
        body: JSON.stringify(payload)
    });

    const result = await resp.json();
    if (resp.status === 201 && result.data && result.data.key) {
        console.log(`[SUCCESS] Draft created: https://note.com/n/${result.data.key}`);
        return result.data.key;
    } else {
        const msg = result.error ? result.error.message : 'Unknown error';
        console.error(`[FAILURE] Status ${resp.status}: ${msg}`);
        if (msg === 'not_login') {
            console.warn('[HINT] Your session cookies in note_projects/cookies.json might be expired.');
        }
        throw new Error('Upload failed: ' + msg);
    }
}

// CLI support
if (require.main === module) {
    const filePath = process.argv[2] || '/home/s0u7a/.openclaw/workspace/note_projects/articles/third_article.md';
    uploadDraft(filePath).catch(err => {
        // console.error(err.message);
        process.exit(1);
    });
}

module.exports = { uploadDraft };
