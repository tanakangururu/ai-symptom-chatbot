/**
 * Sangoma Health Bot - Production Ready
 * A Telegram bot that helps identify illnesses based on symptoms
 * 
 * Developer: Tanaka Ngururu
 */

require("dotenv").config();
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
const http = require('http');

// ============================================
// HEROKU WEB SERVER (keeps the app alive)
// ============================================
const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sangoma Health Bot</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                h1 { color: #2e7d32; }
                .status { background: #e8f5e9; padding: 15px; border-radius: 8px; }
                a { color: #1976d2; }
            </style>
        </head>
        <body>
            <h1>🏥 Sangoma Health Bot</h1>
            <div class="status">
                <p><strong>Status:</strong> ✅ Running</p>
                <p><strong>Platform:</strong> Telegram</p>
                <p><strong>Conditions:</strong> 12 illnesses supported</p>
            </div>
            <p>Chat with the bot on Telegram: <a href="https://t.me/sangoma_x7k2_bot">@sangoma_x7k2_bot</a></p>
            <p><em>Developer: Tanaka Ngururu</em></p>
        </body>
        </html>
    `);
});

server.listen(PORT, () => {
    console.log(`🌐 Web server running on port ${PORT}`);
});

const chatWithOpenAI = require("./openaiApi");
const systemPrompt = require("./prompt");
const symptomsData = require("./symptoms.json");

// ============================================
// CONFIGURATION - Check for bot token
// ============================================
let TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;

// In-memory session state per chat
const sessions = {};

// ============================================
// Telegram Bot API Helper
// ============================================
async function botApiRequest(method, body = {}) {
    const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/${method}`;

    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    const data = await res.json();

    if (!data.ok) {
        console.error(`Telegram API Error [${method}]:`, data.description);
        throw new Error(data.description || "Telegram Bot API error");
    }

    return data.result;
}

// ============================================
// Build the complete system prompt with symptoms database
// ============================================
function buildSystemPrompt() {
    const illnessDetails = symptomsData.illnesses.map(illness => {
        return `
### ${illness.name}
- Description: ${illness.description}
- Temperature: ${illness.temperature_range}
- Onset: ${illness.onset}
- Duration: ${illness.duration}
- Severity: ${illness.severity}
- Symptoms: ${illness.symptoms.join(", ")}`;
    }).join("\n");

    const quickList = symptomsData.illnesses.map((illness, i) =>
        `${i + 1}. ${illness.name}`
    ).join("\n");

    return `${systemPrompt}

══════════════════════════════════════════
YOUR MEDICAL DATABASE - ${symptomsData.illnesses.length} CONDITIONS
══════════════════════════════════════════

Quick Reference:
${quickList}

══════════════════════════════════════════
DETAILED ILLNESS INFORMATION
══════════════════════════════════════════
${illnessDetails}

══════════════════════════════════════════
FOLLOW-UP QUESTIONS BY SYMPTOM
══════════════════════════════════════════
${JSON.stringify(symptomsData.symptom_questions, null, 2)}

══════════════════════════════════════════
DIAGNOSIS GUIDELINES
══════════════════════════════════════════

1. ALWAYS check symptoms against ALL ${symptomsData.illnesses.length} conditions
2. Ask about TEMPERATURE - it's crucial for differential diagnosis:
   - No fever: Consider Migraine, Allergic Rhinitis, Common Cold
   - Low fever (37-38°C): Common Cold, Gastroenteritis
   - Moderate fever (38-39°C): Flu, COVID-19, Chickenpox
   - High fever (39°C+): Malaria, Typhoid, Pneumonia, Strep Throat

3. Ask about ONSET:
   - Sudden: Flu, Strep Throat, Gastroenteritis
   - Gradual: COVID-19, Mononucleosis, Typhoid

4. Consider UNIQUE symptoms:
   - Loss of taste/smell → COVID-19
   - Cyclical fever with chills → Malaria
   - Itchy rash with blisters → Chickenpox
   - One-sided throbbing headache → Migraine
   - White patches on tonsils → Strep Throat
   - Extreme fatigue lasting weeks → Mononucleosis

5. When giving diagnosis, ALWAYS list multiple possibilities if symptoms overlap

══════════════════════════════════════════
RAW DATABASE (for reference)
══════════════════════════════════════════
${JSON.stringify(symptomsData, null, 2)}`;
}

// ============================================
// Initialize or reset user session
// ============================================
function initializeSession(chatId) {
    const fullSystemPrompt = buildSystemPrompt();

    sessions[chatId] = {
        conversation: [
            { role: "system", content: fullSystemPrompt }
        ],
        startedAt: new Date().toISOString()
    };

    console.log(`✅ Session initialized for chat ${chatId}`);
}

// ============================================
// Handle bot commands
// ============================================
async function handleCommand(chatId, command, firstName) {
    switch (command) {
        case "/start":
            initializeSession(chatId);
            const illnessNames = symptomsData.illnesses.map(i => i.name).join(", ");
            await botApiRequest("sendMessage", {
                chat_id: chatId,
                text: `Hello ${firstName}! 👋\n\nI'm *Sangoma*, your AI health assistant.\n\n🏥 I can help identify *${symptomsData.illnesses.length} different conditions* including:\n${illnessNames}\n\n⚠️ *Disclaimer:* I provide guidance only, not medical diagnoses. Always consult a healthcare professional.\n\n📝 *Commands:*\n/start - New consultation\n/reset - Clear history\n/help - Show commands\n/illnesses - List all conditions\n\nWhat symptoms are you experiencing?`,
                parse_mode: "Markdown"
            });
            return true;

        case "/reset":
            initializeSession(chatId);
            await botApiRequest("sendMessage", {
                chat_id: chatId,
                text: "🔄 Conversation reset!\n\nWhat symptoms are you experiencing?",
            });
            return true;

        case "/help":
            await botApiRequest("sendMessage", {
                chat_id: chatId,
                text: `📋 *Commands:*\n\n/start - New consultation\n/reset - Clear history\n/illnesses - List conditions\n/help - Show this message\n\n💡 *Tips:*\n• Mention your temperature\n• Describe duration\n• Rate severity (1-10)\n• Note if sudden or gradual onset`,
                parse_mode: "Markdown"
            });
            return true;

        case "/illnesses":
            const list = symptomsData.illnesses.map((illness, i) =>
                `${i + 1}. *${illness.name}*\n   ${illness.symptoms.slice(0, 3).join(", ")}...`
            ).join("\n\n");

            await botApiRequest("sendMessage", {
                chat_id: chatId,
                text: `🏥 *Conditions I Can Identify:*\n\n${list}`,
                parse_mode: "Markdown"
            });
            return true;

        default:
            return false;
    }
}

// ============================================
// Process user message and get AI response
// ============================================
async function processMessage(chatId, text, firstName) {
    if (!sessions[chatId]) {
        initializeSession(chatId);
    }

    sessions[chatId].conversation.push({ role: "user", content: text });

    await botApiRequest("sendChatAction", {
        chat_id: chatId,
        action: "typing"
    });

    try {
        const reply = await chatWithOpenAI(sessions[chatId].conversation);
        sessions[chatId].conversation.push({ role: "assistant", content: reply });

        // Split long messages (Telegram limit: 4096 chars)
        if (reply.length > 4000) {
            const chunks = reply.match(/.{1,4000}/gs) || [reply];
            for (const chunk of chunks) {
                await botApiRequest("sendMessage", { chat_id: chatId, text: chunk });
            }
        } else {
            await botApiRequest("sendMessage", { chat_id: chatId, text: reply });
        }

        console.log(`📤 Response sent to ${firstName}`);

    } catch (error) {
        console.error(`❌ Error for ${firstName}:`, error.message);
        await botApiRequest("sendMessage", {
            chat_id: chatId,
            text: "Sorry, I encountered an error. Please try again or use /reset."
        });
    }
}

// ============================================
// Main polling loop
// ============================================
async function pollMessages() {
    console.log("📡 Listening for messages...\n");
    let lastUpdateId = 0;

    while (true) {
        try {
            const updates = await botApiRequest("getUpdates", {
                offset: lastUpdateId + 1,
                timeout: 30,
                allowed_updates: ["message"]
            });

            for (const update of updates) {
                lastUpdateId = update.update_id;

                if (!update.message || !update.message.text) continue;

                const text = update.message.text.trim();
                const chatId = update.message.chat.id;
                const firstName = update.message.from?.first_name || "User";

                console.log(`📨 ${firstName}: ${text}`);

                if (text.startsWith("/")) {
                    const command = text.split(" ")[0].toLowerCase();
                    const handled = await handleCommand(chatId, command, firstName);
                    if (handled) continue;
                }

                await processMessage(chatId, text, firstName);
            }

        } catch (err) {
            console.error("❌ Polling error:", err.message);
            await new Promise(r => setTimeout(r, 5000));
        }
    }
}

// ============================================
// STARTUP WITH INTERACTIVE SETUP
// ============================================
const readline = require("readline");

function createReadlineInterface() {
    return readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
}

function askQuestion(rl, question) {
    return new Promise(resolve => rl.question(question, resolve));
}

async function interactiveSetup() {
    const rl = createReadlineInterface();
    const fs = require("fs");

    console.log("\n┌─────────────────────────────────────────────────┐");
    console.log("│         SANGOMA BOT - FIRST TIME SETUP          │");
    console.log("└─────────────────────────────────────────────────┘\n");

    console.log("You need a Telegram Bot Token. Here's how to get one:\n");
    console.log("  1. Open Telegram on your phone/desktop");
    console.log("  2. Search for: @BotFather");
    console.log("  3. Send the message: /newbot");
    console.log("  4. Follow the prompts to name your bot");
    console.log("  5. BotFather will give you a token like:");
    console.log("     7123456789:AAHxR2Jxxxxxxxxxxxxxxxxxx\n");

    const token = await askQuestion(rl, "Paste your Bot Token here: ");

    if (!token || token.trim().length < 20) {
        console.log("\n❌ Invalid token. Please try again.");
        rl.close();
        process.exit(1);
    }

    // Check if we need OpenAI key too
    let openaiKey = process.env.OPENAI_API_KEY;
    if (!openaiKey) {
        console.log("\nYou also need an OpenAI API key.");
        console.log("Get one from: https://platform.openai.com/api-keys\n");
        openaiKey = await askQuestion(rl, "Paste your OpenAI API Key here: ");
    }

    rl.close();

    // Save to .env file
    const envContent = `OPENAI_API_KEY=${openaiKey.trim()}\nTELEGRAM_BOT_TOKEN=${token.trim()}\n`;

    try {
        fs.writeFileSync(".env", envContent);
        console.log("\n✅ Saved to .env file!");
        console.log("\nRestarting bot...\n");

        // Update process.env for current session
        process.env.TELEGRAM_BOT_TOKEN = token.trim();
        process.env.OPENAI_API_KEY = openaiKey.trim();

        return true;
    } catch (err) {
        console.error("❌ Could not save .env file:", err.message);
        console.log("\nManually create a .env file with:");
        console.log(`OPENAI_API_KEY=${openaiKey.trim()}`);
        console.log(`TELEGRAM_BOT_TOKEN=${token.trim()}`);
        process.exit(1);
    }
}

async function main() {
    console.log("═══════════════════════════════════════════");
    console.log("   SANGOMA HEALTH BOT");
    console.log("   Developer: Tanaka Ngururu");
    console.log("═══════════════════════════════════════════\n");

    // Check if TELEGRAM_BOT_TOKEN is missing or empty
    if (!TELEGRAM_BOT_TOKEN || TELEGRAM_BOT_TOKEN.trim() === "" || TELEGRAM_BOT_TOKEN === "your-telegram-bot-token-here") {
        console.log("⚠️  TELEGRAM_BOT_TOKEN not found in .env file\n");
        await interactiveSetup();
    }

    // Re-read environment after potential setup
    require("dotenv").config({ override: true });
    TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;

    if (!TELEGRAM_BOT_TOKEN) {
        console.error("❌ Still missing TELEGRAM_BOT_TOKEN. Please restart.");
        process.exit(1);
    }

    // Check OpenAI key
    if (!process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY.trim() === "") {
        console.log("⚠️  OPENAI_API_KEY not found in .env file\n");
        await interactiveSetup();
        require("dotenv").config({ override: true });
    }

    // Check symptoms database
    if (!symptomsData?.illnesses?.length) {
        console.error("❌ symptoms.json is missing or empty!");
        process.exit(1);
    }

    // Try to connect
    console.log("Connecting to Telegram...");

    try {
        const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe`;
        const res = await fetch(url, { method: "POST" });
        const data = await res.json();

        if (!data.ok) {
            console.error("\n❌ Invalid Bot Token:", data.description);
            console.log("\nYour token doesn't work. Let's get a new one.\n");
            await interactiveSetup();

            // Reload and retry
            require("dotenv").config({ override: true });
            TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;

            const retryRes = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe`, { method: "POST" });
            const retryData = await retryRes.json();

            if (!retryData.ok) {
                throw new Error(retryData.description || "Invalid token");
            }

            console.log(`\n✅ Bot: @${retryData.result.username}`);
        } else {
            console.log(`\n✅ Bot: @${data.result.username}`);
        }

        console.log(`✅ Database: ${symptomsData.illnesses.length} illnesses loaded`);
        console.log(`✅ OpenAI: Ready\n`);

        // Start listening
        pollMessages();

    } catch (err) {
        console.error("\n❌ Failed to connect:", err.message);
        console.log("\nPlease check your TELEGRAM_BOT_TOKEN and try again.");
        process.exit(1);
    }
}

main();