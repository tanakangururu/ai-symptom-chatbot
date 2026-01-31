/**
 * OpenAI API Integration
 * Handles communication with GPT models
 */

require("dotenv").config();
const OpenAI = require("openai");

const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

async function chatWithOpenAI(conversation) {
    try {
        const response = await client.chat.completions.create({
            model: "gpt-4o-mini",
            messages: conversation,
            max_tokens: 1500,
            temperature: 0.7,
        });

        return response.choices[0].message.content;

    } catch (error) {
        console.error("OpenAI Error:", error.message);

        if (error.code === 'insufficient_quota') {
            return "I'm temporarily unavailable due to API limits. Please try again later.";
        }
        if (error.code === 'invalid_api_key') {
            return "Configuration error. Please contact support.";
        }

        return "I encountered an error. Please try again.";
    }
}

module.exports = chatWithOpenAI;