const express = require('express');
const { Ultraviolet } = require('@titaniumnetwork-dev/ultraviolet');
const path = require('path');

const app = express();
const uv = new Ultraviolet();

app.use('/', express.static(path.join(__dirname, 'public')));
app.use('/uv', uv.middleware);

app.get('/proxy/:path', async (req, res) => {
    const path = req.params.path;
    let url = path.startsWith('http://') || path.startsWith('https://') ? path : `http://${path}`;

    try {
        const proxyResponse = await uv.fetch(url, {
            method: req.method,
            headers: req.headers,
            body: req.body
        });

        res.status(proxyResponse.status)
            .set(proxyResponse.headers)
            .send(proxyResponse.body);

    } catch (e) {
        res.status(500).send(`An error occurred while requesting ${url}: ${e.message}`);
    }
});

const port = process.env.PORT || 8000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
