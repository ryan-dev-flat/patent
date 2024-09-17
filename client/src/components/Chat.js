// src/Chat.js
import React, { useState } from 'react';
import axios from 'axios';

function Chat({ token }) {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [patents, setPatents] = useState([]);

    const sendMessage = async () => {
        const res = await axios.post('http://localhost:5000/chat', { message }, {
            headers: { Authorization: `Bearer ${token}` }
        });
        setResponse(res.data.response);
        setPatents(res.data.patents);
    };

    return (
        <div>
            <h2>Chat with GPT</h2>
            <textarea placeholder="Type your message here..." onChange={(e) => setMessage(e.target.value)}></textarea>
            <button onClick={sendMessage}>Send</button>
            <div>
                <h3>Response:</h3>
                <p>{response}</p>
            </div>
            <div>
                <h3>Related Patents:</h3>
                <ul>
                    {patents.map((patent, index) => (
                        <li key={index}>
                            <h4>{patent.title}</h4>
                            <p>{patent.abstract}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default Chat;
