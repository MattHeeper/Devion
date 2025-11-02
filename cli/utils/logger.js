import chalk from 'chalk';

export function success(message) {
  console.log(chalk.green('✅ ' + message));
}

export function error(message) {
  console.log(chalk.red('❌ ' + message));
}

export function warning(message) {
  console.log(chalk.yellow('⚠️  ' + message));
}

export function info(message) {
  console.log(chalk.blue('ℹ️  ' + message));
}

export function header(message) {
  console.log(chalk.bold.cyan('\n' + message + '\n'));
}

export function tool(name, status, version = null) {
  if (status === 'installed') {
    console.log(chalk.green(`  ✅ ${name}: ${version}`));
  } else {
    console.log(chalk.red(`  ❌ ${name}: Not installed`));
  }
}

export function summary(installed, total) {
  console.log(chalk.bold(`\n📊 Summary: ${installed}/${total} tools installed`));
  
  if (installed === total) {
    console.log(chalk.green('🎉 All tools are ready!\n'));
  } else {
    console.log(chalk.yellow(`⚠️  ${total - installed} tools missing\n`));
  }
}