const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');

// TON TOKEN ICI
const token = '8339532089:AAHnTZHjCtzTIqLcdEKXQO3mnz_d2FDBrEs';

const bot = new TelegramBot(token, { polling: true });

// stockage users
let users = [];

// charger si existe déjà
if (fs.existsSync('users.json')) {
    users = JSON.parse(fs.readFileSync('users.json'));
}

// quand quelqu’un parle au bot → on récupère son ID
bot.on('message', (msg) => {
    const chatId = msg.chat.id;

    if (!users.includes(chatId)) {
        users.push(chatId);

        fs.writeFileSync('users.json', JSON.stringify(users));
        console.log("Nouvel utilisateur :", chatId);
    }
})

const ADMIN_ID = 123456789; // TON ID Telegram

bot.onText(/\/broadcast (.+)/, (msg, match) => {
    if (msg.chat.id !== ADMIN_ID) return;

    const message = match[1];

    users.forEach(id => {
        bot.sendMessage(id, message);
    });
});
