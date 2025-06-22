const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 8081;

const server = http.createServer((req, res) => {
    // Parse URL to remove query parameters
    const url = new URL(req.url, `http://localhost:${port}`);
    let filePath = path.join(__dirname, url.pathname === '/' ? 'landing.html' : url.pathname);

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