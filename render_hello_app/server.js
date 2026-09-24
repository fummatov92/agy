const express = require('express');
const app = express();

const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => {
  res.json({
    status: 'ONLINE',
    message: 'Hello World from JarvisOS Render Worker Cloud!',
    platform: 'Render.com (Free Web Service)',
    deployedAt: new Date().toISOString(),
    uptimeSeconds: Math.floor(process.uptime()),
    features: [
      'Render CLI Automated Deployment',
      'Zero Secret Leak Logging',
      'Render History DB Auditing'
    ]
  });
});

app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`🚀 [Hello App] Server ${PORT}-portda ishga tushdi.`);
});
