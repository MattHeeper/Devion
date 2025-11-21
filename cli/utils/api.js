import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

/**
 * ESM workaround for __dirname and __filename.
 */
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Executes a Python command through the core module.
 * * This function acts as the primary bridge between the Node.js CLI and the Python backend.
 * It spawns a child process, executes the specific Devion module, and handles JSON communication.
 * * @param {string} command - The command to execute (e.g., 'status', 'init').
 * @param {object} [args={}] - Optional arguments to pass to the Python module.
 * @returns {Promise<object>} - Resolves with the parsed JSON response from Python.
 */
export function callPython(command, args = {}) {
  return new Promise((resolve, reject) => {
    // Calculate the project root path relative to this file (cli/utils/api.js -> project root)
    const projectRoot = path.resolve(__dirname, '../../');

    // Prepare arguments for the Python executable
    // We use '-m devion.main' to run the package as a module
    const pythonArgs = ['-m', 'devion.main', command, JSON.stringify(args)];

    const pythonProcess = spawn('python3', pythonArgs, {
      cwd: projectRoot,
      env: {
        ...process.env,
        // Critical: Add project root to PYTHONPATH so Python can find the 'devion' package
        PYTHONPATH: projectRoot,
      },
    });

    let stdout = '';
    let stderr = '';

    // Capture standard output
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    // Capture standard error
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    // Handle process exit
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        // Reject if the process failed (non-zero exit code)
        return reject(new Error(`Core process failed with code ${code}.\nDetails: ${stderr}`));
      }

      try {
        // Attempt to parse the JSON response from the core
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (error) {
        // Handle cases where Python output is not valid JSON
        reject(new Error(`Invalid response from Core:\n${stdout}\nParse Error: ${error.message}`));
      }
    });

    // Handle spawn errors (e.g., Python not installed)
    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to spawn Python process: ${error.message}`));
    });
  });
}
