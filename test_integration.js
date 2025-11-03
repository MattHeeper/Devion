import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// فرمان تست
const command = 'help';
const argsJson = '{}';

// مسیر پروژه
const projectRoot = __dirname; // یعنی همون جایی که core داخلشه
const coreMain = path.join(projectRoot, 'core', 'main.py');

console.log('🚀 Running Devion test...');
console.log('📂 Project root:', projectRoot);
console.log('🐍 Core main path:', coreMain);

const python = spawn('python3', ['-m', 'core.main', command, argsJson], {
  cwd: projectRoot,
  env: { ...process.env, PYTHONPATH: projectRoot }, // 🔥 درستش اینه
});

python.stdout.on('data', (data) => {
  console.log('🐍 Python output:', data.toString());
});

python.stderr.on('data', (data) => {
  console.error('❌ Python error:', data.toString());
});

python.on('close', (code) => {
  console.log(`⚙️ Python exited with code ${code}`);
});
