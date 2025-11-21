import chalk from 'chalk';

/**
 * Symbols used for log messages.
 */
const SYMBOLS = {
  success: '✅',
  error: '❌',
  warning: '⚠️ ',
  info: 'ℹ️ ',
  bullet: '•',
};

/**
 * Prints a success message in green.
 * @param {string} message - The message to display.
 */
export function success(message) {
  console.log(chalk.green(`${SYMBOLS.success} ${message}`));
}

/**
 * Prints an error message in red.
 * @param {string} message - The message to display.
 */
export function error(message) {
  console.log(chalk.red(`${SYMBOLS.error} ${message}`));
}

/**
 * Prints a warning message in yellow.
 * @param {string} message - The message to display.
 */
export function warning(message) {
  console.log(chalk.yellow(`${SYMBOLS.warning} ${message}`));
}

/**
 * Prints an informational message in blue.
 * @param {string} message - The message to display.
 */
export function info(message) {
  console.log(chalk.blue(`${SYMBOLS.info} ${message}`));
}

/**
 * Prints a section header in bold cyan.
 * Adds vertical padding for better readability.
 * @param {string} title - The section title.
 */
export function header(title) {
  console.log('\n' + chalk.bold.cyan(title) + '\n');
}

/**
 * Prints the status of a specific tool.
 * @param {string} name - The name of the tool (e.g., 'python').
 * @param {string} status - The status ('installed' or 'not-installed').
 * @param {string|null} [version=null] - The version string if installed.
 */
export function tool(name, status, version = null) {
  if (status === 'installed') {
    console.log(
      chalk.green(`  ${SYMBOLS.success} ${chalk.bold(name)}: ${version}`)
    );
  } else {
    console.log(
      chalk.red(`  ${SYMBOLS.error} ${chalk.bold(name)}: Not installed`)
    );
  }
}

/**
 * Prints the final summary of the scan/operation.
 * @param {number} installed - Count of installed tools.
 * @param {number} total - Total number of tools checked.
 */
export function summary(installed, total) {
  console.log(
    chalk.bold(`\n📊 Summary: ${installed}/${total} tools installed`)
  );

  if (installed === total) {
    console.log(chalk.green('🎉 All tools are ready to go!\n'));
  } else {
    const missing = total - installed;
    console.log(chalk.yellow(`${SYMBOLS.warning} ${missing} tools are missing.\n`));
  }
}
