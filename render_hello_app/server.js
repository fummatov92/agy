const express = require('express');
const app = express();

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

app.get('/healthz', (req, res) => {
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`🚀 [Hello App] Server ${PORT}-portda ishga tushdi.`);
});
