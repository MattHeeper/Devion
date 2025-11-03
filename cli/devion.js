#!/usr/bin/env node

import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, ".."); // مسیر پروژه اصلی
const corePath = path.join(projectRoot, "core", "main.py");

const colors = {
  green: "\x1b[32m",
  red: "\x1b[31m",
  yellow: "\x1b[33m",
  blue: "\x1b[36m",
  reset: "\x1b[0m",
};

if (!fs.existsSync(corePath)) {
  console.error(`${colors.red}❌ core/main.py not found!${colors.reset}`);
  process.exit(1);
}

const args = process.argv.slice(2);
const command = args[0];

if (!command) {
  console.log(`${colors.yellow}Usage: devion <command>${colors.reset}`);
  process.exit(0);
}

console.log(`${colors.blue}🚀 Running Devion command:${colors.reset}`, command);

try {
  const output = execSync(`python3 -m core.main ${command}`, {
    cwd: projectRoot, 
    env: {
      ...process.env,
      PYTHONPATH: projectRoot, 
    },
    encoding: "utf-8",
  });

  console.log(`${colors.green}${output}${colors.reset}`);
} catch (error) {
  console.error(`${colors.red}⚠️ Error running command:${colors.reset}`, command);
  console.error(error.stdout || error.message);
  process.exit(1);
}
