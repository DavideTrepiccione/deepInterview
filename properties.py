URL_CHAT ="https://api.openai.com/v1/chat/completions"
API_KEY ="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"
PATH_RESUME=""
PATH_INFO_JOB ="" 
ENGINE = "text-davinci-003"
SYSTEM_PROMPT_SPEECH="Sei un assistente utile che aiuta nella trascrizione di colloqui di lavoro. Il tuo compito è correggere eventuali discrepanze ortografiche nel testo trascritto, assicurandoti che i termini tecnologici in inglese siano scritti correttamente, indipendentemente dalla lingua parlata nell'audio. Fai attenzione a trascrivere correttamente qualsiasi termine tecnico, acronimo o jargon specifico del settore, mantenendo la punteggiatura necessaria come punti, virgole e maiuscole. Usa solo il contesto fornito per effettuare queste correzioni."
SYSTEM_PROMPT_INTERVIEW=""
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

pre {
    background-color: #f7f7f7;
    border: 1px solid #e1e1e8;
    border-left: 3px solid #f36d33;
    padding: 10px 15px;
    border-radius: 4px;
    overflow: auto;
}

code {
    font-family: 'Courier New', monospace;
    font-size: 0.95em;
    background-color: #f7f7f7;
    padding: 2px 4px;
    border-radius: 4px;
}

.message {
    background-color: #ebf5fb;
    padding: 10px;
    border-radius: 4px;
    border-left: 3px solid #d4e6f1;
    margin-bottom: 10px;
    max-width: 80%;
}

.sent {
    background-color: #dff0d8;
    border-color: #d6e9c6;
}

.received {
    background-color: #f2dede;
    border-color: #ebccd1;
}


    </style>
</head>
<body>
    <div id="chat-container" class="chat-container">
        <!-- I messaggi verranno aggiunti qui -->
    </div>
</body>
</html>
"""


































































