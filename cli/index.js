#!/usr/bin/env node

const { Command } = require('commander');
const { runCommand } = require('./utils/api');

// Initialize the command line program
const program = new Command();

program
  .name('devion')
  .description('Devion CLI: Hybrid Development Environment Manager (Node.js Frontend)')
  .version('1.0.0', '-v, --version')
  .allowExcessArguments(false);

// --- Core Commands ---

program
  .command('status')
  .description('Checks the health and version of core development tools (Python, Node, Git, Docker).')
  .action(() => {
    runCommand('status');
  });

program
  .command('scan')
  .description('Performs a deep system scan and reports detailed OS information.')
  .action(() => {
    runCommand('scan');
  });

program
  .command('analyze')
  .description('Analyzes the current project structure and generates file statistics.')
  .action(() => {
    runCommand('analyze');
  });

program
  .command('fix')
  .description('Attempts to fix missing configurations or dependencies.')
  .action((options) => {
    runCommand('fix', options);
  });

program
  .command('deploy')
  .description('Builds and packages the project into a distributable format.')
  .action(() => {
    runCommand('deploy');
  });

program
  .command('config')
  .description('Manages global settings in ~/.devion/config.json.')
  .option('-k, --key <key>', 'Configuration key to modify or view.')
  .option('-v, --value <value>', 'New value to set for the key.')
  .action((options) => {
    runCommand('config', options);
  });

program
  .command('init')
  .description('Re-initializes the global Devion configuration file.')
  .action(() => {
    runCommand('init');
  });

program.parse(process.argv);
