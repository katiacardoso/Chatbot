document.getElementById("chatbot-form").onsubmit = async function(event) {
    event.preventDefault(); // Impede o comportamento padrão do formulário (recarregar a página)

    // Obter a entrada do usuário
    var user_input = document.getElementById("user_input").value;

    try {
        // Fazer uma requisição ao servidor Flask para obter a resposta do chatbot
        var response = await fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: user_input }) // Enviar a entrada do usuário como JSON
        });

        // Verificar se a resposta da requisição foi bem-sucedida
        if (response.ok) {
            // Extrair a resposta do corpo da resposta
            var resposta = await response.text();

            // Atualizar a caixa .chatbot-results com a resposta real e mostrar
            var chatbotResults = document.querySelector(".chatbot-results");
            chatbotResults.innerHTML = 'RESPOSTA: ' + resposta;
            chatbotResults.style.display = "block";
        } else {
            // Em caso de erro na resposta do servidor
            console.error('Erro na resposta do servidor:', response.status);
        }
    } catch (error) {
        // Em caso de erro na requisição
        console.error('Erro na requisição:', error);
    }
};
