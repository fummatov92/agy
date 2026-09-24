/**
 * Local Simulator: VPS WebSocket Ratsiya Shtabi & Orchestrator
 */
const WebSocket = require('ws');

const PORT = 15855;
const wss = new WebSocket.Server({ port: PORT });

console.log(`📡 [VPS Hub Simulator] WebSocket Server ${PORT}-portda ishga tushdi.`);

wss.on('connection', (ws) => {
  console.log('🟢 [VPS Hub] Yangi worker ulandi!');

  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data);
      console.log('📥 [VPS Hub] Xabar olindi:', msg.event, msg);

      if (msg.event === 'worker:ready') {
        console.log(`✅ [VPS Hub] Worker ro'yxatga olindi: ${msg.workerId}`);
        
        // Simulyatsiya: 1 soniyadan keyin test vazifa berish
        setTimeout(() => {
          console.log(`📤 [VPS Hub] ${msg.workerId} ga vazifa yuborilmoqda...`);
          ws.send(JSON.stringify({
            event: 'task:assign',
            payload: {
              taskId: 'TASK-CLUSTER-001',
              taskName: 'Repository Security Audit Test',
              targetUrl: 'github.com/fummatov92/agy'
            }
          }));
        }, 1000);
      }

      if (msg.event === 'task:completed') {
        console.log(`🎉 [VPS Hub] VAZIFA YAKUNLANDI! Worker: ${msg.workerId}, Report ID: ${msg.reportId}`);
        console.log(`🤖 [VPS Hub] 'agy -p' ga uzatuvchi trigger muvaffaqiyatli ishga tushdi.`);
        process.exit(0);
      }
    } catch (e) {
      console.error('Xatolik:', e.message);
    }
  });
});
