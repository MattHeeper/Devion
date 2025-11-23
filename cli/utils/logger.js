// Basic ANSI Color Codes for robust CLI output
const colors = {
    Reset: "\x1b[0m",
    Bright: "\x1b[1m",
    FgRed: "\x1b[31m",
    FgGreen: "\x1b[32m",
    FgYellow: "\x1b[33m",
    FgCyan: "\x1b[36m",
};

/**
 * Utility function for standardized logging.
 * @param {string} color ANSI color code.
 * @param {string} prefix Icon and label for the log type.
 * @param {string} message The main message to log.
 * @param {any[]} args Additional arguments to pass to console.log.
 */
function log(color, prefix, message, ...args) {
    // Outputs in the format: [COLOR][BRIGHT] [PREFIX] [RESET] message
    console.log(`${colors.Bright}${color}${prefix}${colors.Reset} ${message}`, ...args);
}

function logInfo(message, ...args) {
    log(colors.FgCyan, 'ℹ️  INFO:', message, ...args);
}

function logSuccess(message, ...args) {
    log(colors.FgGreen, '✅ SUCCESS:', message, ...args);
}

function logError(message, ...args) {
    log(colors.FgRed, '❌ ERROR:', message, ...args);
}

function logWarning(message, ...args) {
    log(colors.FgYellow, '⚠️  WARNING:', message, ...args);
}

// Export functions using CommonJS syntax
module.exports = {
    logInfo,
    logSuccess,
    logError,
    logWarning
};
