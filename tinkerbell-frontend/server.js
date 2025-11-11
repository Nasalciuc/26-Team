const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 8081;

const server = http.createServer((req, res) => {
    // Parse URL to remove query parameters
    const url = new URL(req.url, `http://localhost:${port}`);
    let filePath;
    
    // Route mapping
    if (url.pathname === '/') {
        filePath = path.join(__dirname, 'landing.html');
    } else if (url.pathname === '/app') {
        filePath = path.join(__dirname, 'index.html');
    } else if (url.pathname === '/dashboard') {
        filePath = path.join(__dirname, 'dashboard.html');
    } else {
        filePath = path.join(__dirname, url.pathname);
    }

    const extname = path.extname(filePath);
    let contentType = 'text/html';

    switch (extname) {
        case '.css':
            contentType = 'text/css';
            break;
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.html':
            contentType = 'text/html';
            break;
        case '.png':
            contentType = 'image/png';
            break;
        case '.svg':
            contentType = 'image/svg+xml';
            break;
    }

    fs.readFile(filePath, (err, content) => {
        if (err) {
            if (err.code === 'ENOENT') {
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end('Server error');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        }
    });
});

server.listen(port, () => {
    console.log(`Frontend server running at http://localhost:${port}/`);
});