import { Command } from 'commander';
import ora from 'ora';
import { callPython } from './utils/api.js'; // Import the clean API bridge
import * as logger from './utils/logger.js'; // Import the logger utilities

const program = new Command();

/**
 * Executes a command by calling the Python core, managing the spinner and output.
 * This centralized function ensures all command executions have consistent error handling and UI feedback.
 * @param {string} command - The command verb to send to Python (e.g., 'status', 'analyze').
 * @param {object} args - Arguments derived from commander options.
 */
async function executeCommand(command, args) {
  const spinner = ora(`Running ${command} command...`).start();

  try {
    // Call the Python core via the bridge
    const result = await callPython(command, args);
    spinner.succeed(`Command ${command} finished successfully.`);
    
    // Display result based on the command type (simplified logging for now)
    if (result.success) {
      logger.header(`\n✨ Devion ${command} Report`);
      logger.info(JSON.stringify(result.data, null, 2));
    } else {
      logger.error(`Operation failed: ${result.message}`);
      if (result.errors && result.errors.length) {
        result.errors.forEach(err => logger.info(`- ${err}`));
      }
    }
    
  } catch (error) {
    spinner.fail(`Command ${command} failed.`);
    // Log the detailed error from the API/Python process
    logger.error(error.message);
  }
}

/**
 * Defines the main program metadata and commands.
 */
function setupCommands() {
  program
    .name('devion')
    .version('1.0.0', '-v, --version')
    .description('Devion: A Hybrid CLI tool for environment management and analysis.')
    .action(() => {
        // Default action shows help
        program.help();
    });

  // --- 1. Status Command ---
  program
    .command('status')
    .description('Checks the installation status of all required tools and dependencies.')
    .action(() => {
      // The command verb passed to Python is 'status'
      executeCommand('status', {});
    });

  // --- 2. Analyze Command ---
  program
    .command('analyze')
    .description('Scans the project for architectural issues and dependency conflicts.')
    .option('-f, --format <type>', 'Specify output format (e.g., json, cli)', 'cli')
    .action((options) => {
      // The command verb passed to Python is 'analyze'
      executeCommand('analyze', { format: options.format });
    });
    
  // Add other commands (e.g., init, fix, deploy) following this pattern
}

/**
 * Main entry point function.
 */
export function run() {
  setupCommands();
  program.parse(process.argv);
}

// Execute the main run function
run();
