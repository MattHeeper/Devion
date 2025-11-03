
import { Command } from 'commander';
import ora from 'ora';
import * as logger from './utils/logger.js';
import { callPython } from './utils/api.js';

const program = new Command();

program
  .name('devion')
  .description('Devion - Development Environment Manager')
  .version('1.0.0');

program
  .command('status')
  .description('Check development environment status')
  .option('-v, --verbose', 'Show detailed information')
  .action(async (options) => {
    const spinner = ora('Checking system...').start();

    try {
      const result = await callPython('status', { verbose: options.verbose });

      spinner.stop();

      if (result.success) {
        logger.header('🔧 Development Environment Status');

        const tools = result.data.tools;
        for (const [name, info] of Object.entries(tools)) {
          if (info.installed) {
            logger.tool(name, 'installed', info.version);
          } else {
            logger.tool(name, 'not-installed');
          }
        }

        const summary = result.data.summary;
        logger.summary(summary.installed, summary.total);
      } else {
        logger.error(result.message);
        if (result.errors.length > 0) {
          result.errors.forEach(err => logger.error(`  ${err}`));
        }
        process.exit(1);
      }
    } catch (error) {
      spinner.stop();
      logger.error(`Failed to check status: ${error.message}`);
      process.exit(1);
    }
  });

program.parse();