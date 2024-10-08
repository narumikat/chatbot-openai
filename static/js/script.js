$(document).ready(function () {
    $('#record-btn').click(function () {
        $('#status').text('Recording audio...');
        $.ajax({
            url: '/send',
            type: 'POST',
            success: function (data) {
                $('#status').text('Recording completed!');

                setTimeout(function () {
                    $('#status').text('Record new audio');
                }, 3000);

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

                const audioElement = document.getElementById('audio-response');
                audioElement.src = data.audio_file; // Atualiza para o novo arquivo de áudio
                audioElement.load(); // Carrega o novo src
                audioElement.playbackRate = 1.8;
                audioElement.play(); // Toca o áudio

                $('#chat-history').animate({scrollTop: $('#chat-history')[0].scrollHeight}, 500);
            },
        });
    });
});
