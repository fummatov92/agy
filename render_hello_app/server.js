const express = require('express');
const app = express();
app.use(express.json());

const os = require('os');
const fs = require('fs');

const PORT = process.env.PORT || 10000;

function readSystemFile(path) {
  try {
    if (fs.existsSync(path)) {
      return fs.readFileSync(path, 'utf8').trim();
    }
  } catch (e) {
    return null;
  }
  return null;
}

function getCgroupMemory() {
  // cgroups v1
  const v1Limit = readSystemFile('/sys/fs/cgroup/memory/memory.limit_in_bytes');
  const v1Usage = readSystemFile('/sys/fs/cgroup/memory/memory.usage_in_bytes');
  
  // cgroups v2
  const v2Limit = readSystemFile('/sys/fs/cgroup/memory.max');
  const v2Usage = readSystemFile('/sys/fs/cgroup/memory.current');

  let limitBytes = null;
  let usageBytes = null;
  let cgroupVersion = 'none';

  if (v2Limit && v2Limit !== 'max') {
    limitBytes = parseInt(v2Limit, 10);
    usageBytes = parseInt(v2Usage || '0', 10);
    cgroupVersion = 'v2';
  } else if (v1Limit && parseInt(v1Limit, 10) < 9000000000000000) {
    limitBytes = parseInt(v1Limit, 10);
    usageBytes = parseInt(v1Usage || '0', 10);
    cgroupVersion = 'v1';
  }

  return {
    cgroupVersion,
    limitMb: limitBytes ? Math.round(limitBytes / (1024 * 1024)) : null,
    usageMb: usageBytes ? Math.round(usageBytes / (1024 * 1024)) : null
  };
}

function testMaxAllocatableRam() {
  const chunks = [];
  const chunkSizeMb = 10;
  let allocatedMb = 0;
  const maxTestMb = 450; // Safety cap below 512MB to prevent hard OOM crash

  try {
    while (allocatedMb < maxTestMb) {
      // Allocate 10MB chunk and fill to ensure memory is physically committed
      const buf = Buffer.alloc(chunkSizeMb * 1024 * 1024, 1);
      chunks.push(buf);
      allocatedMb += chunkSizeMb;
    }
  } catch (err) {
    // Allocation hit limit
  }

  const resultMb = allocatedMb;
  // Clear buffers immediately to release memory
  chunks.length = 0;
  if (global.gc) {
    try { global.gc(); } catch (e) {}
  }

  return resultMb;
}

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
      'Render History DB Auditing',
      'Live RAM Probing (/api/ram-probe)'
    ]
  });
});

app.get('/api/ram-probe', (req, res) => {
  const memUsage = process.memoryUsage();
  const cgroup = getCgroupMemory();
  const maxTestedAllocMb = testMaxAllocatableRam();
  
  const toMb = (bytes) => (bytes / (1024 * 1024)).toFixed(2);

  res.json({
    status: 'SUCCESS',
    timestamp: new Date().toISOString(),
    platform: {
      platform: process.platform,
      arch: process.arch,
      nodeVersion: process.version,
      cpuCount: os.cpus().length,
      cpuModel: os.cpus()[0]?.model || 'Unknown'
    },
    osMemory: {
      totalHostMemoryMb: toMb(os.totalmem()),
      freeHostMemoryMb: toMb(os.freemem())
    },
    containerCgroupLimits: {
      cgroupVersion: cgroup.cgroupVersion,
      containerLimitMb: cgroup.limitMb ? `${cgroup.limitMb} MB` : 'Unlimited / Host Level',
      containerUsageMb: cgroup.usageMb ? `${cgroup.usageMb} MB` : 'N/A'
    },
    nodeProcessMemory: {
      rssMb: toMb(memUsage.rss),
      heapTotalMb: toMb(memUsage.heapTotal),
      heapUsedMb: toMb(memUsage.heapUsed),
      externalMb: toMb(memUsage.external),
      arrayBuffersMb: toMb(memUsage.arrayBuffers || 0)
    },
    ramStressTest: {
      safeMaxAllocatedMb: `${maxTestedAllocMb} MB`,
      verdict: maxTestedAllocMb >= 400 ? 'Render Free Plan (512MB RAM) ichida 400+ MB bemalol ajratila oladi.' : `Konteynerda ajratilgan maksimal xavfsiz RAM: ${maxTestedAllocMb} MB`
    }
  });
});

const path = require('path');
const { execSync, exec } = require('child_process');

const AGY_BIN = path.join(__dirname, 'bin', 'agy');

// Auto-restore headless OAuth token and device profile if provided via environment
function restoreAgyAuth() {
  const geminiDir = path.join(os.homedir(), '.gemini', 'antigravity-cli');
  if (!fs.existsSync(geminiDir)) {
    fs.mkdirSync(geminiDir, { recursive: true });
  }

  let tokenRestored = false;
  if (process.env.AGY_OAUTH_TOKEN_B64) {
    try {
      const tokenPath = path.join(geminiDir, 'antigravity-oauth-token');
      fs.writeFileSync(tokenPath, Buffer.from(process.env.AGY_OAUTH_TOKEN_B64, 'base64'));
      tokenRestored = true;
    } catch (e) {
      console.error('Failed to restore AGY OAuth token:', e.message);
    }
  }

  if (process.env.AGY_INSTALLATION_ID) {
    try {
      fs.writeFileSync(path.join(geminiDir, 'installation_id'), process.env.AGY_INSTALLATION_ID.trim());
    } catch (e) {}
  }

  if (process.env.AGY_SETTINGS_B64) {
    try {
      fs.writeFileSync(path.join(geminiDir, 'settings.json'), Buffer.from(process.env.AGY_SETTINGS_B64, 'base64'));
    } catch (e) {}
  }

  return tokenRestored;
}

restoreAgyAuth();

app.get('/api/agy/status', (req, res) => {
  const binaryExists = fs.existsSync(AGY_BIN);
  let binarySizeMb = 0;
  let versionOutput = null;
  let execError = null;

  if (binaryExists) {
    try {
      const stats = fs.statSync(AGY_BIN);
      binarySizeMb = (stats.size / (1024 * 1024)).toFixed(2);
      versionOutput = execSync(`"${AGY_BIN}" --version`, { timeout: 10000 }).toString().trim();
    } catch (e) {
      execError = e.message;
      if (e.stdout) versionOutput = e.stdout.toString().trim();
    }
  }

  const tokenExists = fs.existsSync(path.join(os.homedir(), '.gemini', 'antigravity-cli', 'antigravity-oauth-token'));

  res.json({
    status: 'SUCCESS',
    installed: binaryExists,
    binaryPath: AGY_BIN,
    binarySize: `${binarySizeMb} MB`,
    version: versionOutput || 'N/A',
    error: execError,
    authenticated: tokenExists,
    environment: {
      hasEnvToken: !!process.env.AGY_OAUTH_TOKEN_B64,
      nodeVersion: process.version,
      platform: process.platform,
      arch: process.arch
    }
  });
});

app.get('/api/agy/help', (req, res) => {
  if (!fs.existsSync(AGY_BIN)) {
    return res.status(404).json({ error: 'agy binary not installed' });
  }

  try {
    const helpOutput = execSync(`"${AGY_BIN}" --help`, { timeout: 10000 }).toString();
    res.type('text/plain').send(helpOutput);
  } catch (e) {
    res.status(500).json({ error: e.message, stderr: e.stderr?.toString() });
  }
});

app.post('/api/agy/exec', (req, res) => {
  const { prompt } = req.body || {};
  if (!prompt) {
    return res.status(400).json({ error: 'prompt is required in JSON body' });
  }

  if (!fs.existsSync(AGY_BIN)) {
    return res.status(404).json({ error: 'agy binary not installed' });
  }

  const sanitizedPrompt = prompt.replace(/"/g, '\\"');
  const cmd = `"${AGY_BIN}" -p "${sanitizedPrompt}"`;

  exec(cmd, { timeout: 60000, maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
    if (err) {
      return res.status(500).json({
        ok: false,
        error: err.message,
        stdout: stdout ? stdout.trim() : '',
        stderr: stderr ? stderr.trim() : ''
      });
    }

    res.json({
      ok: true,
      stdout: stdout.trim(),
      stderr: stderr ? stderr.trim() : ''
    });
  });
});

app.get('/api/agy/test', (req, res) => {
  const prompt = req.query.prompt || 'Respond with only the word OK';
  if (!fs.existsSync(AGY_BIN)) {
    return res.status(404).json({ error: 'agy binary not installed' });
  }

  const cmd = `"${AGY_BIN}" -p "${prompt.replace(/"/g, '\\"')}"`;
  exec(cmd, { timeout: 60000, maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
    res.json({
      ok: !err,
      exitCode: err ? err.code : 0,
      error: err ? err.message : null,
      stdout: stdout ? stdout.trim() : '',
      stderr: stderr ? stderr.trim() : ''
    });
  });
});

app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`🚀 [Hello App] Server ${PORT}-portda ishga tushdi.`);
});
