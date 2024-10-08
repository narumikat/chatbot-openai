$(document).ready(function () {
    $('#record-btn').click(function () {
        $('#status').text('Recording audio...');
        $.ajax({
            url: '/send',
            type: 'POST',
            success: function (data) {
                $('#status').text('Recording completed!');

                // Adiciona a mensagem do usuário
                $('#chat-history').append(`
                    <div class="d-flex align-items-center justify-content-end">
                        <div class="user-msg">
                            <p>${data.transcription}</p>
                        </div>
                        <img src="${userPhotoUrl}" alt="Avatar" class="avatar ms-2">
                    </div>
                `);

                // Adiciona a resposta do ChatGPT
                $('#chat-history').append(`
                    <div class="d-flex align-items-center justify-content-start">
                        <img src="${chatGptLogoUrl}" alt="Avatar" class="avatar me-2">
                        <div class="chatgpt-msg">
                            <p>${data.chatgpt_response}</p>
                        </div>
                    </div>
                `);

                // Rolando para o final do histórico de mensagens
                $('#chat-history').animate({scrollTop: $('#chat-history')[0].scrollHeight}, 500);
            },
            error: function () {
                $('#status').text('Erro ao gravar áudio');
            }
        });
    });
});
