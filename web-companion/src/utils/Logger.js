/**
 * Logger utility for the Pyodide Interactive Companion
 */

class Logger {
    static LEVELS = {
        DEBUG: 0,
        INFO: 1,
        WARN: 2,
        ERROR: 3
    };

    static currentLevel = Logger.LEVELS.WARN;

    static setLevel(level) {
        Logger.currentLevel = level;
    }

    static formatMessage(level, message, data = null) {
        const timestamp = new Date().toISOString();
        const levelName = Object.keys(Logger.LEVELS).find(key => Logger.LEVELS[key] === level);

        let formatted = '';
        if (level >= Logger.LEVELS.WARN) {
            formatted = `[${timestamp}] ${levelName}: ${message}`;
        } else {
            formatted = `${levelName}: ${message}`;
        }

        if (data) {
            if (typeof data === 'object') {
                formatted += `\n${JSON.stringify(data, null, 2)}`;
            } else {
                formatted += ` ${data}`;
            }
        }

        return formatted;
    }

    static debug(message, data = null) {
        if (Logger.currentLevel <= Logger.LEVELS.DEBUG) {
            console.debug(Logger.formatMessage(Logger.LEVELS.DEBUG, message, data));
        }
    }

    static info(message, data = null) {
        if (Logger.currentLevel <= Logger.LEVELS.INFO) {
            console.info(Logger.formatMessage(Logger.LEVELS.INFO, message, data));
        }
    }

    static warn(message, data = null) {
        if (Logger.currentLevel <= Logger.LEVELS.WARN) {
            console.warn(Logger.formatMessage(Logger.LEVELS.WARN, message, data));
        }
    }

    static error(message, error = null) {
        if (Logger.currentLevel <= Logger.LEVELS.ERROR) {
            console.error(Logger.formatMessage(Logger.LEVELS.ERROR, message, error));
        }
    }

    static group(label) {
        console.group(label);
    }

    static groupEnd() {
        console.groupEnd();
    }
}

export { Logger }; 