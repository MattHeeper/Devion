import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function callPython(command, args = {}) {
  return new Promise((resolve, reject) => {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    
    // اضافه کردن پوشه‌ی 'core' به PYTHONPATH
    const corePath = path.join(__dirname, '../../core');
    
    const argsJson = JSON.stringify(args);
    
    const python = spawn('python3', ['-m', 'core.main', command, argsJson], {
      cwd: path.join(__dirname, '../..'),
      env: { ...process.env, PYTHONPATH: corePath }  // اضافه کردن مسیر core به محیط
    });

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    python.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}\n${stderr}`));
        return;
      }

      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (error) {
        reject(new Error(`Failed to parse Python output: ${error.message}\n${stdout}`));
      }
    });

    python.on('error', (error) => {
      reject(new Error(`Failed to start Python: ${error.message}`));
    });
  });
}
