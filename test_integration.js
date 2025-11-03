import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const command = 'help';
const argsJson = '{}'

const corePath = path.join(__dirname, 'core');

console.log('🔧 Running `status` command...');
console.log('📂 Current working dir:', process.cwd());
console.log('🐍 Core path:', corePath);

const python = spawn('python3', ['-m', 'core.main', command, argsJson], {
  cwd: __dirname, 
  env: { ...process.env, PYTHONPATH: corePath },
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

