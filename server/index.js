const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { Configuration, OpenAIApi } = require('openai');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Replace with your OpenAI API Key
const openai = new OpenAIApi(new Configuration({
  apiKey: process.env.OPENAI_API_KEY
}));

app.post('/api/chat', async (req, res) => {
  const { message, language } = req.body;

  const prompt = `
You are a helpful financial chatbot assistant called FinanichChat speaking to a Kenyan in ${language}.
Give advice in simple ${language} on:
- Saving
- Debt
- Loans
- Business ideas

User: ${message}
Answer:
`;

  try {
    const completion = await openai.createChatCompletion({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7
    });

    res.json({ reply: completion.data.choices[0].message.content });
  } catch (error) {
    console.error("OpenAI error:", error.message);
    res.status(500).json({ error: 'Failed to generate response' });
  }
});

app.listen(5000, () => console.log("Server running on port 5000"));
