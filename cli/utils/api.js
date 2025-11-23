const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const { logError, logSuccess, logInfo } = require('./logger');

/**
 * Helper to detect the correct Python executable.
 * Looks for the virtual environment relative to the installation directory.
 */
function getPythonExecutable() {
  // Calculate project root based on the location of this file (cli/utils/api.js)
  // We go up two levels: cli/utils -> cli -> root
  const projectRoot = path.resolve(__dirname, '../../');
  
  // 1. Check for Linux/macOS virtual environment in the project root
  const unixVenv = path.join(projectRoot, '.venv', 'bin', 'python');
  if (fs.existsSync(unixVenv)) {
    return unixVenv;
  }

  // 2. Check for Windows virtual environment in the project root
  const winVenv = path.join(projectRoot, '.venv', 'Scripts', 'python.exe');
  if (fs.existsSync(winVenv)) {
    return winVenv;
  }

  // 3. Fallback to system python (only works if installed globally or in active venv)
  return 'python3';
}

/**
 * Executes a command in the Python core backend.
 * @param {string} command The Devion command name (e.g., 'status', 'analyze').
 * @param {object} options CLI options passed to the command.
 */
function runCommand(command, options = {}) {
  const optionsJson = JSON.stringify(options);
  const pythonExecutable = getPythonExecutable();
  
  // Arguments for the Python core
  const commandArgs = [
      '-m', 
      'devion.main', 
      command, 
      optionsJson 
  ]; 

  logInfo(`Executing Python core: ${pythonExecutable} ${commandArgs.join(' ')}`);

  // We keep cwd as process.cwd() so commands run in the user's current folder,
  // but we execute using the Python from our internal venv.
  const pythonProcess = spawn(pythonExecutable, commandArgs, {
    cwd: process.cwd()
  });

  pythonProcess.stdout.on('data', (data) => {
    try {
      const output = data.toString().trim();
      // Try to parse output as JSON to pretty print if needed
      const jsonOutput = JSON.parse(output);
      
      if (jsonOutput.success) {
          logSuccess('Operation Successful:', JSON.stringify(jsonOutput.data, null, 2));
          if(jsonOutput.message) console.log(jsonOutput.message);
      } else {
          logError('Operation Failed:', jsonOutput.message);
          if (jsonOutput.errors && jsonOutput.errors.length > 0) {
              jsonOutput.errors.forEach(err => console.error(`- ${err}`));
          }
      }
    } catch (e) {
      // If output isn't JSON (e.g. print statements), just show it
      console.log(data.toString());
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    logError('Python Core Error:', data.toString());
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      logError(`Python process exited with code ${code}`);
    }
  });
}

module.exports = {
  runCommand
};
